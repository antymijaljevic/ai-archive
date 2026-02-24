---
paths:
  - "src/api/**/*.ts"
  - "src/pages/api/**/*.ts"
  - "app/api/**/*.ts"
---

# API Conventions

These rules apply specifically to API route handlers and endpoints.

## REST API Conventions

### HTTP Methods

Use appropriate HTTP methods:

- **GET** - Retrieve data (never modify)
- **POST** - Create new resource
- **PUT** - Replace entire resource
- **PATCH** - Partially update resource
- **DELETE** - Remove resource

```typescript
// Good
app.get('/api/users/:id', getUser);        // Retrieve
app.post('/api/users', createUser);        // Create
app.put('/api/users/:id', updateUser);     // Full update
app.patch('/api/users/:id', patchUser);    // Partial update
app.delete('/api/users/:id', deleteUser);  // Delete

// Bad - using POST for everything
app.post('/api/getUser', getUser);
app.post('/api/deleteUser', deleteUser);
```

### URL Structure

```typescript
// Good - RESTful, hierarchical
GET    /api/users
GET    /api/users/:id
POST   /api/users
PUT    /api/users/:id
DELETE /api/users/:id
GET    /api/users/:id/posts
POST   /api/users/:id/posts

// Bad - non-RESTful
GET    /api/getAllUsers
GET    /api/getUserById/:id
POST   /api/createNewUser
POST   /api/deleteUser
```

### Response Format

Use consistent response format across all endpoints:

```typescript
// Success response
type SuccessResponse<T> = {
  data: T;
  error: null;
  meta?: {
    page?: number;
    limit?: number;
    total?: number;
  };
};

// Error response
type ErrorResponse = {
  data: null;
  error: {
    code: string;
    message: string;
    details?: unknown;
  };
};

// Example
export async function getUser(req, res) {
  try {
    const user = await db.users.findOne(req.params.id);

    if (!user) {
      return res.status(404).json({
        data: null,
        error: {
          code: 'USER_NOT_FOUND',
          message: 'User not found'
        }
      });
    }

    return res.status(200).json({
      data: user,
      error: null
    });
  } catch (error) {
    return res.status(500).json({
      data: null,
      error: {
        code: 'INTERNAL_ERROR',
        message: 'An unexpected error occurred'
      }
    });
  }
}
```

## Status Codes

Use appropriate HTTP status codes:

```typescript
// Success
200 OK              // Successful GET, PUT, PATCH
201 Created         // Successful POST
204 No Content      // Successful DELETE

// Client Errors
400 Bad Request     // Invalid input/validation error
401 Unauthorized    // Not authenticated
403 Forbidden       // Authenticated but not authorized
404 Not Found       // Resource doesn't exist
409 Conflict        // Conflict with current state (duplicate)
422 Unprocessable   // Validation failed
429 Too Many Requests // Rate limit exceeded

// Server Errors
500 Internal Error  // Unexpected server error
503 Service Unavailable // Temporary downtime
```

## Input Validation

Always validate request data:

```typescript
import { z } from 'zod';

// Define schema
const createUserSchema = z.object({
  email: z.string().email(),
  name: z.string().min(2).max(100),
  age: z.number().int().min(18).optional()
});

// Validate in handler
export async function createUser(req, res) {
  try {
    // Validate input
    const data = createUserSchema.parse(req.body);

    // Create user with validated data
    const user = await db.users.create(data);

    return res.status(201).json({
      data: user,
      error: null
    });
  } catch (error) {
    if (error instanceof z.ZodError) {
      return res.status(400).json({
        data: null,
        error: {
          code: 'VALIDATION_ERROR',
          message: 'Invalid input',
          details: error.errors
        }
      });
    }

    return res.status(500).json({
      data: null,
      error: {
        code: 'INTERNAL_ERROR',
        message: 'An unexpected error occurred'
      }
    });
  }
}
```

## Authentication & Authorization

Every protected endpoint must check authentication:

```typescript
// Middleware
export function requireAuth(req, res, next) {
  const token = req.headers.authorization?.replace('Bearer ', '');

  if (!token) {
    return res.status(401).json({
      data: null,
      error: {
        code: 'UNAUTHORIZED',
        message: 'Authentication required'
      }
    });
  }

  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    req.user = decoded;
    next();
  } catch (error) {
    return res.status(401).json({
      data: null,
      error: {
        code: 'INVALID_TOKEN',
        message: 'Invalid or expired token'
      }
    });
  }
}

// Check authorization (not just authentication)
export function requireAdmin(req, res, next) {
  if (!req.user?.isAdmin) {
    return res.status(403).json({
      data: null,
      error: {
        code: 'FORBIDDEN',
        message: 'Admin access required'
      }
    });
  }
  next();
}

// Use in routes
app.get('/api/admin/users', requireAuth, requireAdmin, getAllUsers);
```

## Pagination

For list endpoints, always support pagination:

```typescript
export async function listUsers(req, res) {
  const page = parseInt(req.query.page) || 1;
  const limit = parseInt(req.query.limit) || 20;
  const offset = (page - 1) * limit;

  // Validate limits
  if (limit > 100) {
    return res.status(400).json({
      data: null,
      error: {
        code: 'INVALID_LIMIT',
        message: 'Limit cannot exceed 100'
      }
    });
  }

  const [users, total] = await Promise.all([
    db.users.findMany({ skip: offset, take: limit }),
    db.users.count()
  ]);

  return res.status(200).json({
    data: users,
    error: null,
    meta: {
      page,
      limit,
      total,
      totalPages: Math.ceil(total / limit)
    }
  });
}
```

## Error Handling

Centralized error handling:

```typescript
// Custom error classes
class AppError extends Error {
  constructor(
    public statusCode: number,
    public code: string,
    message: string,
    public details?: unknown
  ) {
    super(message);
  }
}

export class ValidationError extends AppError {
  constructor(message: string, details?: unknown) {
    super(400, 'VALIDATION_ERROR', message, details);
  }
}

export class NotFoundError extends AppError {
  constructor(message: string) {
    super(404, 'NOT_FOUND', message);
  }
}

export class UnauthorizedError extends AppError {
  constructor(message: string) {
    super(401, 'UNAUTHORIZED', message);
  }
}

// Error handler middleware
export function errorHandler(error, req, res, next) {
  if (error instanceof AppError) {
    return res.status(error.statusCode).json({
      data: null,
      error: {
        code: error.code,
        message: error.message,
        details: error.details
      }
    });
  }

  // Log unexpected errors
  console.error('Unexpected error:', error);

  return res.status(500).json({
    data: null,
    error: {
      code: 'INTERNAL_ERROR',
      message: 'An unexpected error occurred'
    }
  });
}

// Use in app
app.use(errorHandler);
```

## API Documentation

Document all endpoints:

```typescript
/**
 * @route GET /api/users/:id
 * @description Get user by ID
 * @access Private (requires authentication)
 * @param {string} id - User ID
 * @returns {User} User object
 * @throws {401} Unauthorized - Not authenticated
 * @throws {404} NotFound - User doesn't exist
 */
export async function getUser(req, res) {
  // Implementation
}
```

## Rate Limiting

Apply rate limits to all public endpoints:

```typescript
import rateLimit from 'express-rate-limit';

const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // 100 requests per window
  message: {
    data: null,
    error: {
      code: 'RATE_LIMIT_EXCEEDED',
      message: 'Too many requests, please try again later'
    }
  }
});

app.use('/api/', limiter);
```

## Logging

Log all API requests:

```typescript
export function requestLogger(req, res, next) {
  const start = Date.now();

  res.on('finish', () => {
    const duration = Date.now() - start;

    logger.info('API Request', {
      method: req.method,
      path: req.path,
      statusCode: res.statusCode,
      duration,
      userId: req.user?.id,
      ip: req.ip
    });
  });

  next();
}

app.use(requestLogger);
```

---

**Auto-loaded**: When working with API files
