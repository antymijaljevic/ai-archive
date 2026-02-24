# Code Style Rules

These rules apply to all code files in the project.

## General Principles

1. **Readability over cleverness** - Write code for humans, not machines
2. **Explicit over implicit** - Be clear about intentions
3. **Consistency over personal preference** - Follow project conventions

## Naming Conventions

### Variables and Functions
```typescript
// Use camelCase
const userName = 'John';
const getUserById = (id: string) => { ... };

// Boolean variables start with is/has/should
const isActive = true;
const hasPermission = false;
const shouldRender = true;

// Constants in UPPER_SNAKE_CASE
const MAX_RETRY_COUNT = 3;
const API_BASE_URL = 'https://api.example.com';
```

### Files and Directories
```
// Components: PascalCase
UserProfile.tsx
LoginForm.tsx

// Utilities: camelCase
dateUtils.ts
apiClient.ts

// Hooks: camelCase with 'use' prefix
useAuth.ts
useFetch.ts

// Tests: Same name + .test
UserProfile.test.tsx
dateUtils.test.ts
```

### Types and Interfaces
```typescript
// Interfaces: PascalCase with 'I' prefix (optional)
interface User {
  id: string;
  name: string;
}

// Types: PascalCase
type UserStatus = 'active' | 'inactive' | 'pending';

// Generics: Single capital letter or descriptive
function map<T>(items: T[]): T[] { ... }
function map<Item>(items: Item[]): Item[] { ... }
```

## Function Guidelines

### Keep Functions Small
```typescript
// Good - focused, single purpose
function validateEmail(email: string): boolean {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

// Bad - doing too much
function processUser(user: User) {
  // 100 lines of code doing many things
}
```

### Use Descriptive Names
```typescript
// Good - clear intent
function calculateTotalPrice(items: Item[]): number { ... }
function sendWelcomeEmail(user: User): Promise<void> { ... }

// Bad - unclear
function calc(arr: any[]): number { ... }
function send(u: any): any { ... }
```

### Prefer Named Parameters for Complex Functions
```typescript
// Good - clear what each parameter means
function createUser({
  name,
  email,
  role = 'user',
  isActive = true
}: CreateUserParams) { ... }

// Bad - unclear what parameters mean
function createUser(name: string, email: string, role: string, isActive: boolean) { ... }
```

## Code Organization

### Import Order
```typescript
// 1. External dependencies
import React from 'react';
import { useState, useEffect } from 'react';

// 2. Internal dependencies (absolute imports)
import { Button } from '@/components/Button';
import { useAuth } from '@/hooks/useAuth';

// 3. Relative imports
import { helper } from './utils';
import styles from './Component.module.css';

// 4. Types
import type { User } from '@/types';
```

### File Structure
```typescript
// 1. Imports
import ...

// 2. Types/Interfaces
interface Props { ... }

// 3. Constants
const DEFAULT_TIMEOUT = 5000;

// 4. Main component/function
export function Component() { ... }

// 5. Helper functions (not exported)
function helperFunction() { ... }

// 6. Styles (if using CSS-in-JS)
const styles = { ... };
```

## Comments

### When to Comment
```typescript
// Good - explains WHY
// Using exponential backoff because API has rate limits
await retryWithBackoff(apiCall);

// Good - explains complex algorithm
// Implementing Dijkstra's algorithm for shortest path
function findShortestPath() { ... }

// Bad - explains WHAT (code is self-explanatory)
// Increment counter by 1
counter++;

// Bad - obvious comment
// Get user by ID
function getUserById(id: string) { ... }
```

### JSDoc for Public APIs
```typescript
/**
 * Fetches user data from the API
 * @param userId - The unique identifier of the user
 * @returns Promise resolving to User object
 * @throws {NotFoundError} When user doesn't exist
 */
export async function fetchUser(userId: string): Promise<User> { ... }
```

## Error Handling

```typescript
// Good - specific error handling
try {
  const user = await fetchUser(userId);
  return user;
} catch (error) {
  if (error instanceof NotFoundError) {
    return null;
  }
  throw error;
}

// Bad - swallowing all errors
try {
  const user = await fetchUser(userId);
  return user;
} catch {
  return null;
}
```

## TypeScript Specific

### Prefer Types Over Any
```typescript
// Good
function processData(data: User[]): ProcessedUser[] { ... }

// Bad
function processData(data: any): any { ... }
```

### Use Type Guards
```typescript
// Good
function isUser(obj: unknown): obj is User {
  return obj !== null && typeof obj === 'object' && 'id' in obj;
}

if (isUser(data)) {
  console.log(data.id); // TypeScript knows this is safe
}
```

### Avoid Non-Null Assertions (!)
```typescript
// Good - handle null case
const user = users.find(u => u.id === id);
if (user) {
  console.log(user.name);
}

// Bad - could cause runtime error
const user = users.find(u => u.id === id)!;
console.log(user.name);
```

## React Specific

### Prefer Function Components
```typescript
// Good
export function UserProfile({ user }: Props) {
  return <div>{user.name}</div>;
}

// Avoid (unless you need lifecycle methods)
export class UserProfile extends React.Component { ... }
```

### Extract Complex JSX
```typescript
// Good - readable
export function UserList({ users }: Props) {
  return (
    <div>
      {users.map(user => (
        <UserCard key={user.id} user={user} />
      ))}
    </div>
  );
}

// Bad - hard to read
export function UserList({ users }: Props) {
  return (
    <div>
      {users.map(user => (
        <div key={user.id}>
          <img src={user.avatar} />
          <h2>{user.name}</h2>
          <p>{user.bio}</p>
          {/* 50 more lines */}
        </div>
      ))}
    </div>
  );
}
```

---

**Auto-loaded**: Always active for all files
