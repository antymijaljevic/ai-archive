# Testing Rules

Testing conventions and requirements for the project.

## General Testing Principles

1. **Tests should be reliable** - Pass consistently, fail only when code is broken
2. **Tests should be fast** - Unit tests in milliseconds, integration tests in seconds
3. **Tests should be isolated** - No dependencies between tests
4. **Tests should be readable** - Clear what's being tested and why

## Test File Structure

```typescript
import { describe, it, expect, beforeEach, afterEach } from 'vitest';
import { render, screen } from '@testing-library/react';
import { MyComponent } from './MyComponent';

describe('MyComponent', () => {
  // Setup
  beforeEach(() => {
    // Common setup
  });

  // Happy path tests first
  describe('when user is logged in', () => {
    it('should display user name', () => {
      // Arrange
      const user = { name: 'John' };

      // Act
      render(<MyComponent user={user} />);

      // Assert
      expect(screen.getByText('John')).toBeInTheDocument();
    });
  });

  // Edge cases
  describe('when user is not logged in', () => {
    it('should display login prompt', () => { ... });
  });

  // Error cases
  describe('when there is an error', () => {
    it('should display error message', () => { ... });
  });
});
```

## Test Naming

Use descriptive test names that explain:
1. What is being tested
2. Under what conditions
3. What the expected outcome is

```typescript
// Good - clear and descriptive
it('should return error when email is invalid')
it('should call onSubmit when form is valid')
it('should disable button while loading')

// Bad - unclear
it('works')
it('test email')
it('button test')
```

## What to Test

### ✅ DO Test

**Business Logic**
```typescript
// Test pure functions
describe('calculateTotalPrice', () => {
  it('should sum item prices', () => {
    const items = [
      { price: 10 },
      { price: 20 }
    ];
    expect(calculateTotalPrice(items)).toBe(30);
  });

  it('should apply discount when provided', () => {
    const items = [{ price: 100 }];
    expect(calculateTotalPrice(items, 0.1)).toBe(90);
  });
});
```

**Component Behavior**
```typescript
describe('LoginForm', () => {
  it('should call onSubmit with email and password', async () => {
    const onSubmit = vi.fn();
    render(<LoginForm onSubmit={onSubmit} />);

    await userEvent.type(screen.getByLabelText('Email'), 'test@example.com');
    await userEvent.type(screen.getByLabelText('Password'), 'password123');
    await userEvent.click(screen.getByRole('button', { name: 'Login' }));

    expect(onSubmit).toHaveBeenCalledWith({
      email: 'test@example.com',
      password: 'password123'
    });
  });
});
```

**Edge Cases**
```typescript
describe('divide', () => {
  it('should return Infinity when dividing by zero', () => {
    expect(divide(10, 0)).toBe(Infinity);
  });

  it('should handle negative numbers', () => {
    expect(divide(-10, 2)).toBe(-5);
  });
});
```

### ❌ DON'T Test

- Implementation details (internal state, private methods)
- Third-party libraries (trust they're tested)
- Trivial code (getters/setters)
- Framework functionality (React, Next.js internals)

## Mocking

### Mock External Dependencies
```typescript
// Mock API calls
vi.mock('./api', () => ({
  fetchUser: vi.fn()
}));

it('should display user data', async () => {
  const mockUser = { id: '1', name: 'John' };
  fetchUser.mockResolvedValue(mockUser);

  render(<UserProfile userId="1" />);

  expect(await screen.findByText('John')).toBeInTheDocument();
});
```

### Keep Mocks Simple
```typescript
// Good - minimal mock
const mockRouter = {
  push: vi.fn()
};

// Bad - over-mocking
const mockRouter = {
  push: vi.fn(),
  replace: vi.fn(),
  back: vi.fn(),
  forward: vi.fn(),
  // ... many unused methods
};
```

## Testing Async Code

```typescript
// Good - use async/await
it('should load user data', async () => {
  render(<UserProfile userId="1" />);

  expect(await screen.findByText('John')).toBeInTheDocument();
});

// Good - wait for specific condition
it('should display error after failed fetch', async () => {
  fetchUser.mockRejectedValue(new Error('Failed'));
  render(<UserProfile userId="1" />);

  await waitFor(() => {
    expect(screen.getByText('Error loading user')).toBeInTheDocument();
  });
});
```

## Test Data

### Use Realistic Data
```typescript
// Good - realistic
const mockUser = {
  id: 'usr_123abc',
  email: 'john.doe@example.com',
  name: 'John Doe',
  createdAt: '2024-01-15T10:30:00Z'
};

// Bad - unrealistic
const mockUser = {
  id: '1',
  email: 'test',
  name: 'test'
};
```

### Use Test Factories
```typescript
// Create reusable test data factories
function createMockUser(overrides = {}) {
  return {
    id: 'usr_123',
    email: 'user@example.com',
    name: 'Test User',
    ...overrides
  };
}

// Use in tests
it('should display admin badge for admin users', () => {
  const admin = createMockUser({ role: 'admin' });
  render(<UserProfile user={admin} />);
  expect(screen.getByText('Admin')).toBeInTheDocument();
});
```

## Coverage Requirements

- **Unit tests**: Aim for >80% coverage on business logic
- **Integration tests**: Cover critical user flows
- **E2E tests**: Cover main user journeys

```bash
# Run tests with coverage
npm run test:coverage

# Coverage should pass these thresholds
{
  "branches": 80,
  "functions": 80,
  "lines": 80,
  "statements": 80
}
```

## Test Organization

```
src/
├── components/
│   ├── Button/
│   │   ├── Button.tsx
│   │   └── Button.test.tsx      # Component tests
│   └── Form/
│       ├── Form.tsx
│       └── Form.test.tsx
├── utils/
│   ├── dateUtils.ts
│   └── dateUtils.test.ts        # Utility tests
└── __tests__/
    ├── integration/             # Integration tests
    │   └── userFlow.test.ts
    └── e2e/                     # E2E tests
        └── checkout.test.ts
```

## Performance Testing

```typescript
// Test that expensive operations are memoized
it('should not recalculate when props unchanged', () => {
  const calculateExpensive = vi.fn(() => 42);
  const { rerender } = render(<Component calculate={calculateExpensive} data={data} />);

  expect(calculateExpensive).toHaveBeenCalledTimes(1);

  rerender(<Component calculate={calculateExpensive} data={data} />);

  // Should still be 1 (memoized)
  expect(calculateExpensive).toHaveBeenCalledTimes(1);
});
```

## Testing Best Practices

1. **AAA Pattern**: Arrange, Act, Assert
2. **One assertion per test** (when possible)
3. **Test behavior, not implementation**
4. **Use meaningful test data**
5. **Clean up after tests** (reset mocks, clear storage)
6. **Run tests before committing**

---

**Auto-loaded**: When working with test files
