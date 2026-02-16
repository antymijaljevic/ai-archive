# Project: [Your Project Name]

<!--
This file contains project-wide conventions and instructions for Claude Code.
Keep it concise and focused on what Claude can't figure out from code alone.
-->

## Quick Info

- **Language**: [e.g., TypeScript, Python, Rust]
- **Framework**: [e.g., React, Next.js, FastAPI]
- **Package Manager**: [e.g., npm, pnpm, yarn, pip]
- **Node Version**: [e.g., 20.x]

## Commands

```bash
# Development
npm run dev                 # Start dev server
npm run build               # Build for production
npm run test                # Run all tests
npm run test:watch          # Watch mode
npm run lint                # Lint code
npm run format              # Format code

# Database (if applicable)
npm run db:migrate          # Run migrations
npm run db:seed             # Seed database
npm run db:reset            # Reset database

# Deployment (if applicable)
npm run deploy:staging      # Deploy to staging
npm run deploy:production   # Deploy to production
```

## Code Style

- Use functional components with hooks (React)
- Prefer `async/await` over promise chains
- Use named exports over default exports
- Keep functions small and focused (max 50 lines)
- Write tests for all business logic
- Use descriptive variable names (no single letters except in loops)

## Project Structure

```
src/
├── components/         # Reusable UI components
├── pages/             # Page components (Next.js) or routes
├── api/               # API client and endpoints
├── hooks/             # Custom React hooks
├── utils/             # Utility functions
├── types/             # TypeScript types
├── styles/            # Global styles
└── config/            # Configuration files
```

## Architecture Decisions

<!-- Explain non-obvious choices -->

- **State Management**: Using Zustand (not Redux - lighter weight, less boilerplate)
- **Styling**: Tailwind CSS with custom design tokens
- **API Calls**: React Query for caching and data fetching
- **Testing**: Vitest + React Testing Library (faster than Jest)
- **Forms**: React Hook Form (better performance than Formik)

## Git Workflow

- Branch naming: `feature/description`, `fix/description`, `chore/description`
- Always create PR for review (no direct commits to main)
- Squash commits before merging
- Run tests before pushing: `npm run test`
- PR title format: `[Feature/Fix/Chore] Description`

## Testing

- All new features need tests
- Test files: `*.test.ts` or `*.test.tsx`
- Run tests before committing
- Aim for >80% coverage on business logic
- Use descriptive test names: `it('should return error when user not found')`

## Environment Variables

**Required:**
- `DATABASE_URL` - Database connection string
- `API_KEY` - External API key
- `JWT_SECRET` - For authentication

**Optional:**
- `DEBUG=true` - Enable verbose logging
- `PORT=3000` - Override default port

**Setup:**
```bash
cp .env.example .env
# Then fill in your values
```

## Common Gotchas

- API responses are always wrapped in `{ data, error }` format
- All dates are UTC timestamps (convert to user timezone in UI)
- File uploads limited to 10MB
- Rate limiting: 100 requests/minute per user
- Database migrations must be reversible (include `down()` method)

## External Services

- **Authentication**: Auth0
- **Database**: PostgreSQL
- **Cache**: Redis
- **File Storage**: AWS S3
- **Error Tracking**: Sentry
- **Analytics**: PostHog

## Useful Links

- [API Documentation](./docs/api.md)
- [Design System](https://www.figma.com/...)
- [Deployment Guide](./docs/deployment.md)
- [Contributing Guidelines](./CONTRIBUTING.md)

## Team Conventions

- Code reviews within 24 hours
- Daily standup at 10am
- Deploy to staging on PR merge
- Production deploys on Fridays (emergency fixes anytime)
- Slack channel: #dev-team

---

**Note**: For personal project preferences, use `CLAUDE.local.md` (gitignored)
