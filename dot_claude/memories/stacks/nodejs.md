# Node.js Development Stack

## Core Toolchain

### Package Management
**Prefer pnpm for performance and disk efficiency, npm as fallback.**

```bash
# Project initialization
npm init -y                   # Create package.json quickly
pnpm init                     # Alternative with pnpm

# Dependency management
pnpm add package-name         # Add runtime dependency
pnpm add -D eslint            # Add development dependency
pnpm add -E react@18.2.0      # Add exact version

# Alternative with npm
npm install package-name      # Runtime dependency
npm install --save-dev eslint # Development dependency
npm install --save-exact react@18.2.0  # Exact version
```

### Project Structure Convention
```
project-name/
├── package.json              # Project configuration and scripts
├── pnpm-lock.yaml           # Lock file (or package-lock.json)
├── tsconfig.json            # TypeScript configuration
├── .eslintrc.js             # ESLint configuration
├── .prettierrc              # Prettier configuration
├── README.md                # Project documentation
├── src/                     # Source code
│   ├── index.ts             # Entry point
│   ├── types/               # Type definitions
│   ├── utils/               # Utility functions
│   └── components/          # Components (if React/Vue)
├── tests/                   # Test suite
│   ├── setup.ts             # Test setup
│   └── __tests__/           # Test files
├── dist/                    # Compiled output (gitignored)
└── node_modules/            # Dependencies (gitignored)
```

## TypeScript Configuration

### TypeScript Setup
```bash
# Install TypeScript
pnpm add -D typescript @types/node ts-node

# Initialize TypeScript config
npx tsc --init
```

### tsconfig.json Configuration
```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "node",
    "lib": ["ES2022"],
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,
    "removeComments": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "exactOptionalPropertyTypes": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "noUncheckedIndexedAccess": true,
    "resolveJsonModule": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist", "tests"]
}
```

## Code Quality Tools

### ESLint Configuration
```bash
# Install ESLint with TypeScript support
pnpm add -D eslint @typescript-eslint/parser @typescript-eslint/eslint-plugin

# Initialize ESLint config
npx eslint --init
```

### .eslintrc.js Configuration
```javascript
module.exports = {
  parser: '@typescript-eslint/parser',
  extends: [
    'eslint:recommended',
    '@typescript-eslint/recommended',
    '@typescript-eslint/recommended-requiring-type-checking',
  ],
  parserOptions: {
    ecmaVersion: 2022,
    sourceType: 'module',
    project: './tsconfig.json',
  },
  rules: {
    '@typescript-eslint/no-unused-vars': 'error',
    '@typescript-eslint/explicit-function-return-type': 'warn',
    '@typescript-eslint/no-explicit-any': 'error',
    'prefer-const': 'error',
    'no-var': 'error',
  },
};
```

### Prettier Configuration
```bash
# Install Prettier
pnpm add -D prettier eslint-config-prettier

# .prettierrc
{
  "semi": true,
  "trailingComma": "es5",
  "singleQuote": true,
  "printWidth": 80,
  "tabWidth": 2,
  "useTabs": false
}
```

## Testing Framework

### Jest with TypeScript
```bash
# Install Jest with TypeScript support
pnpm add -D jest @types/jest ts-jest @jest/globals

# Initialize Jest config
npx jest --init
```

### jest.config.js Configuration
```javascript
module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'node',
  roots: ['<rootDir>/src', '<rootDir>/tests'],
  testMatch: ['**/__tests__/**/*.test.ts', '**/?(*.)+(spec|test).ts'],
  collectCoverageFrom: [
    'src/**/*.ts',
    '!src/**/*.d.ts',
    '!src/**/*.test.ts',
  ],
  coverageDirectory: 'coverage',
  coverageReporters: ['text', 'lcov', 'html'],
};
```

### Test Patterns
```typescript
// tests/__tests__/utils.test.ts
import { describe, it, expect, beforeEach, jest } from '@jest/globals';
import { processData } from '../../src/utils/processor';

describe('processData', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('should process valid data correctly', () => {
    const input = 'test data';
    const result = processData(input);
    
    expect(result).toBeDefined();
    expect(result.status).toBe('success');
  });

  it('should handle invalid input', () => {
    expect(() => processData('')).toThrow('Invalid input');
  });

  it('should handle async operations', async () => {
    const result = await processAsyncData('test');
    expect(result).resolves.toBeDefined();
  });
});
```

## Development Workflow

### Package.json Scripts
```json
{
  "scripts": {
    "dev": "ts-node src/index.ts",
    "build": "tsc",
    "start": "node dist/index.js",
    "test": "jest",
    "test:watch": "jest --watch",
    "test:coverage": "jest --coverage",
    "lint": "eslint src/**/*.ts",
    "lint:fix": "eslint src/**/*.ts --fix",
    "format": "prettier --write src/**/*.ts",
    "type-check": "tsc --noEmit",
    "clean": "rm -rf dist coverage",
    "prebuild": "npm run clean && npm run lint && npm run type-check",
    "prestart": "npm run build"
  }
}
```

### Daily Development Commands
```bash
# Start development
pnpm install                  # Install dependencies
pnpm run dev                  # Start development server

# Development cycle
pnpm run lint:fix            # Fix linting issues
pnpm run format              # Format code
pnpm run type-check          # Check types
pnpm run test                # Run tests

# Before committing
pnpm run lint                # Final lint check
pnpm run test:coverage       # Test with coverage
pnpm run build               # Ensure builds successfully
```

## Framework-Specific Patterns

### Express.js API Server
```bash
# Install Express with TypeScript
pnpm add express
pnpm add -D @types/express

# Basic server setup
import express, { Request, Response, NextFunction } from 'express';

const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());

app.get('/api/health', (req: Request, res: Response) => {
  res.json({ status: 'healthy', timestamp: new Date().toISOString() });
});

// Error handling middleware
app.use((err: Error, req: Request, res: Response, next: NextFunction) => {
  console.error(err.stack);
  res.status(500).json({ error: 'Internal server error' });
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
```

### React/Next.js Setup
```bash
# Create Next.js project with TypeScript
npx create-next-app@latest --typescript project-name

# Or add React to existing project
pnpm add react react-dom
pnpm add -D @types/react @types/react-dom
```

## Performance and Optimization

### Build Optimization
```javascript
// webpack.config.js for custom builds
const path = require('path');

module.exports = {
  mode: 'production',
  entry: './src/index.ts',
  output: {
    path: path.resolve(__dirname, 'dist'),
    filename: 'bundle.js',
  },
  resolve: {
    extensions: ['.ts', '.js'],
  },
  module: {
    rules: [
      {
        test: /\.ts$/,
        use: 'ts-loader',
        exclude: /node_modules/,
      },
    ],
  },
  optimization: {
    minimize: true,
    splitChunks: {
      chunks: 'all',
    },
  },
};
```

### Node.js Performance Patterns
```typescript
// Async/await patterns
async function processItems(items: string[]): Promise<string[]> {
  // Parallel processing
  const results = await Promise.all(
    items.map(item => processItem(item))
  );
  return results;
}

// Stream processing for large data
import { Transform } from 'stream';

const processStream = new Transform({
  objectMode: true,
  transform(chunk, encoding, callback) {
    // Process chunk
    this.push(processChunk(chunk));
    callback();
  },
});
```

## Environment and Configuration

### Environment Variables
```bash
# Install dotenv for development
pnpm add -D dotenv

# .env file
NODE_ENV=development
DATABASE_URL=postgres://localhost:5432/myapp
API_KEY=your-api-key-here
PORT=3000
```

```typescript
// src/config/env.ts
import dotenv from 'dotenv';

if (process.env.NODE_ENV !== 'production') {
  dotenv.config();
}

export const config = {
  nodeEnv: process.env.NODE_ENV || 'development',
  port: parseInt(process.env.PORT || '3000', 10),
  databaseUrl: process.env.DATABASE_URL || '',
  apiKey: process.env.API_KEY || '',
} as const;

// Validate required environment variables
const requiredEnvVars = ['DATABASE_URL', 'API_KEY'] as const;
for (const envVar of requiredEnvVars) {
  if (!process.env[envVar]) {
    throw new Error(`Missing required environment variable: ${envVar}`);
  }
}
```

## Database Integration

### Prisma ORM Setup
```bash
# Install Prisma
pnpm add prisma @prisma/client
npx prisma init

# Generate client after schema changes
npx prisma generate
npx prisma db push
```

### Database Query Patterns
```typescript
// src/db/client.ts
import { PrismaClient } from '@prisma/client';

export const prisma = new PrismaClient({
  log: process.env.NODE_ENV === 'development' ? ['query'] : [],
});

// Graceful shutdown
process.on('beforeExit', async () => {
  await prisma.$disconnect();
});

// src/models/user.ts
export async function createUser(data: { email: string; name: string }) {
  return prisma.user.create({
    data,
    select: {
      id: true,
      email: true,
      name: true,
      createdAt: true,
    },
  });
}
```

## Error Handling and Logging

### Structured Logging
```bash
# Install winston for production logging
pnpm add winston
```

```typescript
// src/utils/logger.ts
import winston from 'winston';

export const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.errors({ stack: true }),
    winston.format.json()
  ),
  transports: [
    new winston.transports.File({ filename: 'error.log', level: 'error' }),
    new winston.transports.File({ filename: 'combined.log' }),
  ],
});

if (process.env.NODE_ENV !== 'production') {
  logger.add(new winston.transports.Console({
    format: winston.format.simple()
  }));
}
```

### Error Handling Patterns
```typescript
// src/utils/errors.ts
export class AppError extends Error {
  constructor(
    message: string,
    public statusCode: number = 500,
    public code?: string
  ) {
    super(message);
    this.name = 'AppError';
  }
}

export function handleAsyncError<T>(
  fn: (...args: any[]) => Promise<T>
) {
  return (...args: any[]): Promise<T> => {
    return Promise.resolve(fn(...args)).catch((error) => {
      logger.error('Async error:', error);
      throw error;
    });
  };
}
```

This module provides comprehensive Node.js development patterns with TypeScript, modern tooling, and production-ready practices.