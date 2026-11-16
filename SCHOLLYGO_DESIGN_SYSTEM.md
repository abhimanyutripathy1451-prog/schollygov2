# SchollyGo Design System
## Midnight + Voltage Yellow

The current SchollyGo visual identity is a high-contrast, premium, dark-mode-first aesthetic. It pairs a deep "Midnight" surface with a high-energy "Voltage Yellow" accent. The design language is engineered to feel like a modern, gamified learning arena—merging serious educational utility with the engaging visual feedback of an esports or gaming platform.

---

# 1. Brand Identity

- **Brand name**: SchollyGo
- **Primary visual concept**: High-contrast, glowing neon accents against deep space/midnight backgrounds.
- **Brand personality**: Competitive, energetic, premium, empowering.
- **Design principles**: High contrast, obvious hierarchy, satisfying micro-interactions, dark-mode native.
- **Intended emotional response**: "I am stepping into an arena to level up." Focus, excitement, and achievement.
- **Primary audience**: Students seeking gamified learning, practice, and test preparation.
- **"Learning Arena" concept**: The platform frames learning as a competitive and rewarding journey (Avatars, Gamertags, XP, Ranks, Streaks).
- **Current brand taglines used in authentication**:
  - Login: "YOUR SYLLABUS. YOUR PRACTICE. YOUR PROGRESS."
  - Signup: "LEARN. PRACTICE. LEVEL UP."

---

# 2. Color System

| Token | Actual Value | Purpose | Where Used |
|---|---|---|---|
| `--color-brand-primary` | `#FACC15` | Voltage Yellow (Primary) | Buttons, focus rings, active tabs, progress bars |
| `--color-brand-hover` | `#FDE047` | Lighter Yellow (Hover) | Button hovers, interactive glows |
| `--color-semantic-success` | `#22C55E` | Positive actions | Available usernames, correct answers |
| `--color-semantic-error` | `#EF4444` | Negative actions | Error banners, invalid inputs |
| `--color-semantic-info` | `#38BDF8` | Information | Informational banners, secondary stats |
| `--color-semantic-rank` | `#A855F7` | Gamification | Rank badges, special achievements |
| `--color-semantic-milestone`| `#F97316` | Gamification | Milestones, streak indicators |
| `--color-ambient-blue` | `rgba(56, 189, 248, 0.05)`| Background effects | Radial glows on backgrounds |
| `--color-ambient-purple` | `rgba(168, 85, 247, 0.05)`| Background effects | Secondary radial glows |
| `--bg-app` | `#080C14` | Main Background | Global page background (Midnight) |
| `--bg-secondary` | `#0F1724` | Secondary Bg | Sidebar, offset sections |
| `--bg-surface` | `#111827` | Card Surface | Main cards, modals, inputs |
| `--bg-surface-elevated` | `#182131` | Elevated Surface | Hover states on cards, inner cards |
| `--text-primary` | `#F8FAFC` | Primary Text | Headings, primary body text |
| `--text-secondary` | `#94A3B8` | Secondary Text | Labels, descriptions, subtitles |
| `--text-muted` | `#64748B` | Muted Text | Placeholder text, disabled text |
| `--border-subtle` | `rgba(255, 255, 255, 0.08)`| Subtle Borders | Card borders, input borders |

**Inconsistencies Noted**:
There is a massive proliferation of hardcoded hex values bypassing the token system:
- `#FBC02D` (a slightly more orange/mustard yellow) is heavily hardcoded across `QuizArena.tsx`, `ChapterView.tsx`, `Dashboard.tsx`, and `AnalyticsView.tsx`.
- `#FACC15` (the official Voltage Yellow) is hardcoded in Auth buttons and some Dashboard text rather than using `var(--color-brand-primary)` or Tailwind's `bg-brand-primary`.
- `#080C14` and `#111827` are hardcoded in Auth layouts instead of using `bg-bg-app` and `bg-bg-surface`.

---

# 3. Background & Ambient Effects

- **Main background**: Deep midnight (`#080C14`), implemented via the `bg-bg-app` class on the `body` tag.
- **Secondary backgrounds**: Used on cards (`#111827`).
- **Radial gradients**: A global radial gradient (`radial-gradient(circle at 50% 0%, rgba(56,189,248,0.05) 0%, transparent 60%)`) sits on the body.
- **Blue/purple/yellow ambient glows**: Large blurred `motion.div` elements (blur-[100px] to blur-[150px]) float in the background of Auth screens.
- **Educational background pattern**: SVG icon pattern (Brain, Timer, Target, etc.).
- **Pattern opacity**: 3% (`opacity-[0.03]`).
- **Gradient opacity**: Glows vary from 40% (`bg-ambient-blue/40`) to 5% (`bg-brand-primary/5`).
- **Glassmorphism effects**: Heavily used on elevated surfaces and hovering cards with `backdrop-blur` and slight white transparent borders `rgba(255,255,255,0.08)`.

---

# 4. Typography System

- **Font family**: `Inter` (sans-serif), `JetBrains Mono` (monospace).
- **Headings**: Highly expressive. Use `font-black`, `tracking-wide` or `tracking-tight`.
- **Labels**: Often `text-xs`, `font-semibold`, `uppercase`, `tracking-wider`.

| Element | Size | Weight | Line Height | Color | Usage |
|---|---:|---:|---:|---|---|
| Card Headers | `text-2xl`/`3xl` | Black (900) | Tight | `#F8FAFC` | Major sections, Modals |
| Subheaders | `text-sm`/`lg` | Semibold (600) | Normal | `#94A3B8` | Descriptions under headers |
| Input Labels | `text-xs` | Semibold (600) | Normal | `#94A3B8` | Forms, Data labels |
| Body Text | `text-sm` | Normal (400) | Relaxed | `#F8FAFC` | General reading text |
| Button Text | `text-sm` | Black (900) | Normal | `#080C14` | Primary CTAs |

---

# 5. Spacing System

- **Page padding**: Usually `p-4 lg:p-8`.
- **Card padding**: Standardized on Auth views as `p-6 md:px-8 md:py-6`. Other cards vary (`p-5`, `p-6`, `p-8`).
- **Form spacing**: `space-y-5` or `space-y-6` between form groups.
- **Input padding**: `p-3.5`.
- **Grid gaps**: Commonly `gap-3` or `gap-6`.

**Consistency**: Spacing mostly relies on Tailwind's default spacing scale (multiples of 0.25rem). However, responsive padding shifts frequently between components.

---

# 6. Border Radius System

- **Buttons**: `rounded-xl` (0.75rem).
- **Inputs**: `rounded-input` (mapped to `0.5rem`).
- **Standard Cards**: `rounded-2xl` (1rem) or `rounded-xl`.
- **Hero/Auth Cards**: `rounded-[2.5rem]` or `rounded-[2rem]` (Highly stylized, heavily rounded).
- **Avatars**: `rounded-[1.25rem]` or `rounded-full`.

---

# 7. Shadows & Elevation

- **Card shadows**: `shadow-2xl` for massive elevation (Auth), `shadow-[0_8px_30px_rgba(250,204,21,0.15)]` for gamified yellow glows.
- **Button shadows**: `shadow-[0_5px_15px_rgba(250,204,21,0.2)]`.
- **Hover elevation**: `-translate-y-1` paired with `shadow-[0_8px_20px_rgba(250,204,21,0.3)]` on Voltage Yellow buttons.
- **Inner shadows**: `shadow-inner` used on inputs and un-elevated cards to simulate depth/recession.

---

# 8. Component Design Language

## Buttons
- **Primary**: Background `#FACC15`, Text `#080C14`, border-bottom 4px (`border-b-[4px]`), rounded-xl, uppercase tracking-widest, font-black.
- **Hover**: Background `#FDE047`, elevates upwards, casts larger yellow shadow.
- **Disabled**: `opacity-40` or `opacity-50`, cursor-not-allowed.

## Inputs
- **Default**: Surface `#111827`, border `rgba(255,255,255,0.08)`, inner shadow.
- **Focus**: Ring `ring-4 ring-brand-primary/20`, border `border-brand-primary`.
- **Error**: Background `bg-semantic-error/10`, border `border-semantic-error/60`, ring `ring-semantic-error/20`, red shadow.

## Cards
- **Surface**: Background `#111827`.
- **Border**: `border border-[rgba(255,255,255,0.08)]`.
- **Hover**: Sometimes introduces a gradient border or a subtle scale transform.

---

# 9. Gamification Visual Language

The gamification system leans heavily into the "Learning Arena" aesthetic. It feels native to SchollyGo, leveraging the same Voltage Yellow and deep dark backgrounds, but turns up the intensity using gradients and drop shadows.

- **XP / Currency**: Usually accompanied by yellow gradients and gold/coin icons.
- **Rank**: Gradients ranging from purple to orange. Badges use heavy `drop-shadow`.
- **Avatars**: Handled via Dicebear (Personas). Placed in heavy borders (`border-[#FBC02D]/50`).
- **Streak**: Represented with flame icons and orange/yellow gradients.

---

# 10. Authentication Experience

- **Login**: Mobile number entry -> Profile selection (Avatar based) -> 4-digit Passkey OTP.
- **Signup**: Persona (Gamertag + Avatar) -> Curriculum (Board/Exam) -> Vault (Name, Mobile, Passkey, Invite Code).
- **Background**: Ambient glows over a subtle 3% opacity educational pattern.
- **Card**: Highly rounded (`2.5rem`), dark surface, white subtle border.
- **CTAs**: Thick, bold, uppercase Voltage Yellow buttons.

---

# 11. Responsive Design Rules

- **Mobile First**: Layouts default to stacked `flex-col`.
- **Breakpoints**: Standard Tailwind breakpoints (`md:`, `lg:`).
- **Container widths**: Auth cards are `max-w-md` (mobile/tablet optimized). Dashboards use full width or `max-w-7xl`.
- **Touch targets**: Inputs (`p-3.5`) and Buttons (`py-4`) easily clear the 44px touch target minimums.

---

# 12. Accessibility

- **WCAG contrast**: PASS (Yellow on Black, White on Dark Blue pass AAA/AA easily).
- **Focus states**: PASS (Thick `ring-4` implementations on inputs).
- **Keyboard navigation**: PARTIAL (Forms submit on enter, but custom interactive divs may lack tabindex).
- **Disabled states**: PASS (`opacity-50`, `disabled` attribute applied).
- **Error states**: PASS (Clear red borders, error text, `aria-live="assertive"` used).
- **Color-only communication**: PARTIAL (Errors use icons + text, but some gamification elements rely heavily on color).
- **Reduced motion**: NOT VERIFIED (Framer motion is used, but no `prefers-reduced-motion` queries observed).

---

# 13. Design Token Usage Audit

### Hardcoded values remaining

| File | Component | Hardcoded Value | Recommended Token | Severity |
|---|---|---|---|---|
| `QuizArena.tsx` | Multiple | `#FBC02D` | `var(--color-brand-primary)` | High |
| `ChapterView.tsx` | Multiple | `#FBC02D` | `var(--color-brand-primary)` | High |
| `Dashboard.tsx` | Multiple | `#FACC15` | `var(--color-brand-primary)` | Medium |
| `LoginView.tsx` | Auth Card | `#111827` | `bg-bg-surface` | Medium |
| `LoginView.tsx` | Button | `#080C14` | `text-bg-app` | Low |

---

# 14. Cross-Page Consistency Audit

- Color consistency: 6/10 (Split personality between `#FACC15` and `#FBC02D`).
- Typography consistency: 8/10 (Strong use of Inter font-black).
- Component consistency: 7/10 (Inputs match in Auth, but diverge slightly in Dashboard).
- Spacing consistency: 7/10.
- Brand consistency: 9/10 (Overall vibe is very strong and distinct).

---

# 15. Design System Exceptions

- **Quiz Arena**: Employs unique background gradients and progress bars not found elsewhere to create a distinct "focus/test" mode.
- **Avatars**: The use of SVG Dicebear avatars introduces flat illustration styles against a glowing neon UI. Transparent backgrounds help bridge this gap.

---

# 16. Current Design System Scorecard

- Brand Identity: 9/10
- Color System: 6/10
- Typography: 8/10
- Spacing: 7/10
- Components: 8/10
- Gamification: 9/10
- Accessibility: 7/10
- Responsive Design: 8/10
- Cross-page consistency: 7/10
- **Overall Design System: 7.6/10**

---

# 17. Review Recommendations

### Critical
- **Problem**: Rogue Yellow Hex (`#FBC02D`).
- **Evidence**: Used heavily in `ChapterView` and `QuizArena` instead of `#FACC15`.
- **Impact**: Causes a subtle "dirty" look when placed near true Voltage Yellow elements.
- **Suggested direction**: Search and replace `#FBC02D` with `var(--color-brand-primary)`.

### High
- **Problem**: Hardcoded surface colors.
- **Evidence**: Auth cards use `bg-[#111827]` instead of `bg-bg-surface`.
- **Impact**: Prevents universal theme switching (e.g., to a Light mode).
- **Suggested direction**: Enforce `bg-bg-surface` across the board.

### Medium
- **Problem**: Input class duplication.
- **Evidence**: The exact same 300-character tailwind class string is copy-pasted 6 times across Login/Signup.
- **Impact**: Maintenance nightmare if input styles need tweaking.
- **Suggested direction**: Extract into a reusable `<Input />` React component.

---

# 18. Design System Change Log

*Document created. Represents the baseline snapshot of the SchollyGo v1.0 UI implementation.*
