# Security Rules

Security requirements and best practices for the project.

## Critical Security Rules

These rules must NEVER be violated:

### 1. Never Commit Secrets

❌ **NEVER** commit:
- API keys
- Database passwords
- JWT secrets
- OAuth tokens
- Private keys
- AWS credentials
- Any sensitive credentials

✅ **ALWAYS**:
- Use environment variables
- Store secrets in `.env` (gitignored)
- Use secret management services (AWS Secrets Manager, Vault)
- Document required env vars in `.env.example`

```bash
# .env (gitignored)
DATABASE_URL=postgresql://localhost/mydb
API_KEY=sk_live_xxxxxxxxxxxxx
JWT_SECRET=super-secret-key

# .env.example (committed)
DATABASE_URL=
API_KEY=
JWT_SECRET=
```

### 2. Always Validate User Input

```typescript
// Good - validated
function createUser(data: unknown) {
  const validated = userSchema.parse(data); // Zod validation
  return db.users.create(validated);
}

// Bad - unvalidated
function createUser(data: any) {
  return db.users.create(data);
}
```

### 3. Use Parameterized Queries

```typescript
// Good - parameterized (safe from SQL injection)
const users = await db.query(
  'SELECT * FROM users WHERE email = $1',
  [email]
);

// Bad - string concatenation (SQL injection risk!)
const users = await db.query(
  `SELECT * FROM users WHERE email = '${email}'`
);
```

### 4. Sanitize HTML Output

```typescript
// Good - React automatically escapes
<div>{userInput}</div>

// Good - DOMPurify for HTML
import DOMPurify from 'dompurify';
<div dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(userHTML) }} />

// Bad - XSS vulnerability!
<div dangerouslySetInnerHTML={{ __html: userInput }} />
```

## Authentication & Authorization

### Password Security

```typescript
// Good - bcrypt with proper salt
import bcrypt from 'bcrypt';

const SALT_ROUNDS = 10;

async function hashPassword(password: string) {
  return bcrypt.hash(password, SALT_ROUNDS);
}

async function verifyPassword(password: string, hash: string) {
  return bcrypt.compare(password, hash);
}

// Bad - weak hashing
import crypto from 'crypto';
const hash = crypto.createHash('md5').update(password).digest('hex');
```

### Password Requirements

Enforce strong passwords:
- Minimum 8 characters
- At least one uppercase letter
- At least one lowercase letter
- At least one number
- At least one special character

```typescript
function validatePassword(password: string): boolean {
  return /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/.test(password);
}
```

### JWT Security

```typescript
// Good - proper JWT handling
import jwt from 'jsonwebtoken';

const JWT_SECRET = process.env.JWT_SECRET!;
const JWT_EXPIRY = '1h';

function createToken(userId: string) {
  return jwt.sign({ userId }, JWT_SECRET, {
    expiresIn: JWT_EXPIRY,
    issuer: 'myapp',
    audience: 'myapp-api'
  });
}

function verifyToken(token: string) {
  try {
    return jwt.verify(token, JWT_SECRET, {
      issuer: 'myapp',
      audience: 'myapp-api'
    });
  } catch (error) {
    return null;
  }
}
```

### Route Protection

```typescript
// Good - middleware checks auth
export async function getServerSideProps(context) {
  const session = await getSession(context);

  if (!session) {
    return {
      redirect: {
        destination: '/login',
        permanent: false
      }
    };
  }

  return { props: { user: session.user } };
}

// Also check authorization (not just authentication)
export async function deleteUser(userId: string, currentUser: User) {
  // Check if user is admin OR deleting their own account
  if (!currentUser.isAdmin && currentUser.id !== userId) {
    throw new UnauthorizedError('Cannot delete other users');
  }

  await db.users.delete(userId);
}
```

## Data Protection

### Sensitive Data in Logs

```typescript
// Good - don't log sensitive data
logger.info('User logged in', { userId: user.id });

// Bad - leaking password!
logger.info('User logged in', { userId: user.id, password: user.password });
```

### Secure Data Transmission

```typescript
// Good - HTTPS only
if (process.env.NODE_ENV === 'production' && !req.secure) {
  return res.redirect(`https://${req.hostname}${req.url}`);
}

// Good - secure cookies
res.cookie('sessionId', sessionId, {
  httpOnly: true,
  secure: true,  // HTTPS only
  sameSite: 'strict',
  maxAge: 3600000
});
```

### CORS Configuration

```typescript
// Good - specific origins
const corsOptions = {
  origin: ['https://myapp.com', 'https://app.myapp.com'],
  credentials: true,
  optionsSuccessStatus: 200
};

app.use(cors(corsOptions));

// Bad - allow all origins with credentials!
app.use(cors({ origin: '*', credentials: true }));
```

## Rate Limiting

Prevent abuse with rate limiting:

```typescript
import rateLimit from 'express-rate-limit';

// General API rate limit
const apiLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // Limit each IP to 100 requests per window
  message: 'Too many requests, please try again later'
});

// Stricter limit for auth endpoints
const authLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 5, // Only 5 login attempts per 15 minutes
  skipSuccessfulRequests: true
});

app.use('/api/', apiLimiter);
app.use('/api/auth/', authLimiter);
```

## File Upload Security

```typescript
// Good - validate file types and size
import multer from 'multer';

const upload = multer({
  limits: {
    fileSize: 10 * 1024 * 1024 // 10MB max
  },
  fileFilter: (req, file, cb) => {
    // Whitelist allowed types
    const allowedTypes = ['image/jpeg', 'image/png', 'image/gif'];

    if (!allowedTypes.includes(file.mimetype)) {
      return cb(new Error('Invalid file type'));
    }

    cb(null, true);
  },
  storage: multer.diskStorage({
    destination: './uploads',
    filename: (req, file, cb) => {
      // Randomize filename to prevent path traversal
      const uniqueSuffix = `${Date.now()}-${Math.random().toString(36).substring(7)}`;
      cb(null, `${uniqueSuffix}-${file.originalname}`);
    }
  })
});
```

## Security Headers

```typescript
import helmet from 'helmet';

app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      styleSrc: ["'self'", "'unsafe-inline'"],
      scriptSrc: ["'self'"],
      imgSrc: ["'self'", 'data:', 'https:'],
    }
  },
  hsts: {
    maxAge: 31536000,
    includeSubDomains: true,
    preload: true
  }
}));
```

## Dependency Security

```bash
# Regularly check for vulnerabilities
npm audit

# Fix vulnerabilities
npm audit fix

# Update dependencies
npm update

# Use exact versions in production
npm install --save-exact
```

## Security Checklist

Before deploying, verify:

- [ ] No secrets in code or git history
- [ ] All user inputs validated
- [ ] SQL queries use parameterization
- [ ] XSS prevention in place
- [ ] Authentication required for protected routes
- [ ] Authorization checks on sensitive operations
- [ ] Passwords hashed with bcrypt/argon2
- [ ] HTTPS enforced in production
- [ ] Security headers configured (helmet)
- [ ] CORS properly configured
- [ ] Rate limiting on auth endpoints
- [ ] File uploads validated
- [ ] Dependencies up-to-date (`npm audit`)
- [ ] Error messages don't leak info
- [ ] Logging doesn't include sensitive data

---

**Auto-loaded**: When working with authentication, API endpoints, or sensitive data

**Resources**:
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [OWASP Cheat Sheets](https://cheatsheetseries.owasp.org/)
