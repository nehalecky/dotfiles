# Visual Feedback Loop Workflow

## Purpose and Scope
For UI/UX development or visual outputs where immediate visual validation is essential.

## When to Use
- UI/UX development with visual components
- Data visualization and chart development
- Frontend component development
- Design implementation and styling
- Visual regression testing
- Responsive design validation
- Animation and interaction development

## Process Flow

**Write Code → Screenshot → Iterate → Perfect**

1. **Write Code:** Implement initial version, focus on core functionality
2. **Screenshot:** Capture current state, document screen sizes, record interactions
3. **Iterate:** Compare with requirements, identify discrepancies, make targeted adjustments
4. **Perfect:** Refine details through rapid cycles, optimize performance, validate accessibility

## Tool Integration

```bash
# Browser screenshots
npx puppeteer-screenshot http://localhost:3000 --output=./screenshots/

# macOS screenshots
screencapture -i ~/Desktop/app-state.png

# Component development
npm run storybook

# Git integration
git commit -m "visual: update component appearance"
```

### Live Development
- Hot reloading for immediate feedback
- Multiple device/browser testing
- Real-time collaboration for design review
- Automated visual regression testing

## Tool Categories

**Web:** Browser DevTools, Puppeteer/Playwright, Storybook, Percy/Chromatic
**Mobile:** Device simulators, real device testing, Figma/Sketch integration
**Desktop:** Platform-specific tools, cross-platform testing, accessibility testing

## Success Criteria
- ✅ Matches design specifications
- ✅ Consistent visual behavior across platforms
- ✅ Smooth user interactions
- ✅ Responsive design works across screen sizes
- ✅ Performance maintains acceptable frame rates

## Common Pitfalls
- ❌ Pixel-perfect obsession over user experience
- ❌ Testing only one device/browser
- ❌ Ignoring accessibility for visual appeal
- ❌ Over-engineering animations (performance hit)
- ❌ Skipping cross-platform validation until late

## Performance Considerations
- Optimize visual assets during iteration
- Monitor frame rates for smooth interactions
- Test on lower-end devices
- Balance visual quality with loading performance

## Feedback Loop Optimization
- Minimize screenshot→code→screenshot time
- Use live reloading for immediate changes
- Set up efficient comparison workflows
- Automate repetitive visual testing

## Integration with Other Workflows
- Often begins with Discovery-First
- May incorporate Test-Driven for component logic
