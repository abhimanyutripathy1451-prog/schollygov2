import {BookOpen, ChevronRight, CircleUserRound, Flame, LogOut, Swords, Target, Tent, Trophy, Zap, BarChart3, Sun, Moon} from 'lucide-react';
import logo from './logo.svg';
import './dashboard.css';

type DashboardUser = {
  full_name: string;
  avatar_seed?: string | null;
  timezone: string;
  curriculum: {name: string; board: string; grade: string; medium: string};
};

type DashboardProps = {
  user: DashboardUser;
  onProfile: () => void;
  onLogout: () => void;
};

function greetingFor(timezone: string) {
  const hour = Number(new Intl.DateTimeFormat('en-GB', {hour: '2-digit', hourCycle: 'h23', timeZone: timezone}).format(new Date()));
  if (hour < 12) return {text: 'Good morning', Icon: Sun};
  if (hour < 17) return {text: 'Good afternoon', Icon: Sun};
  return {text: 'Good evening', Icon: Moon};
}

export function Dashboard({user, onProfile, onLogout}: DashboardProps) {
  const firstName = user.full_name.trim().split(/\s+/)[0] || 'Student';
  const initials = user.full_name.trim().split(/\s+/).slice(0, 2).map(part => part[0]?.toUpperCase()).join('');
  const greeting = greetingFor(user.timezone);
  const GreetingIcon = greeting.Icon;
  return <div className="dashboard-shell">
    <div className="dashboard-glow dashboard-glow-blue" aria-hidden="true" />
    <div className="dashboard-glow dashboard-glow-yellow" aria-hidden="true" />
    <aside className="dashboard-rail" aria-label="Main navigation">
      <div className="dashboard-rail-spacer" />
      <nav>
        <span className="dashboard-rail-item active" aria-current="page" title="Basecamp"><Tent size={25}/><span>Basecamp</span></span>
        <span className="dashboard-rail-item disabled" aria-disabled="true" title="Scorecard coming later"><BarChart3 size={25}/><span>Scorecard</span></span>
        <button className="dashboard-rail-item" type="button" onClick={onProfile} title="My Space"><CircleUserRound size={25}/><span>My Space</span></button>
        <i className="dashboard-rail-divider" />
        <button className="dashboard-rail-item" type="button" onClick={onLogout} title="Log out"><LogOut size={25}/><span>Log out</span></button>
      </nav>
    </aside>
    <div className="dashboard-area">
      <header className="dashboard-header">
        <img src={logo} alt="SchollyGo" className="dashboard-logo" />
        <button className="dashboard-profile" type="button" onClick={onProfile} aria-label={`Open profile for ${user.full_name}`}>
          <span className="dashboard-avatar" aria-hidden="true">{initials}</span>
          <span className="dashboard-profile-copy"><strong>{user.full_name}</strong><small>Student · Grade {user.curriculum.grade}</small></span>
          <ChevronRight size={16} aria-hidden="true" />
        </button>
      </header>
      <main className="dashboard-main">
        <div className="dashboard-content">
          <h1 className="dashboard-greeting"><span>{greeting.text},</span> <strong>{firstName}</strong> <GreetingIcon size={28} aria-hidden="true" /></h1>
          <div className="dashboard-hero-grid">
            <section className="dashboard-quest dashboard-card" aria-labelledby="quest-title">
              <div className="dashboard-quest-copy"><span className="dashboard-eyebrow">Featured Quest</span><h2 id="quest-title">Welcome to the Arena!</h2><p>Your learning journey begins here. Practice activities will appear when your curriculum is ready.</p><button type="button" disabled>Practice coming soon <ChevronRight size={16}/></button></div>
              <div className="dashboard-target" aria-hidden="true"><Target size={46}/></div>
            </section>
            <section className="dashboard-metrics" aria-label="Learning progress">
              <div className="dashboard-card dashboard-metric dashboard-rank"><div className="dashboard-metric-top"><span>Rank & XP</span><Trophy size={17}/></div><strong>—</strong><small>Available when learning starts</small><div className="dashboard-progress-track" aria-hidden="true" /></div>
              <div className="dashboard-card dashboard-metric"><div className="dashboard-metric-top"><span>Mastery</span><Zap size={17}/></div><strong>—</strong><small>No learning data yet</small></div>
              <div className="dashboard-card dashboard-metric"><div className="dashboard-metric-top"><span>Streak</span><Flame size={17}/></div><strong>—</strong><small>No learning data yet</small></div>
            </section>
          </div>
          <section className="dashboard-card dashboard-arsenal" aria-labelledby="arsenal-title">
            <div className="dashboard-arsenal-heading"><div><h2 id="arsenal-title"><Swords size={24}/> My Arsenal</h2><p>{user.curriculum.name} · {user.curriculum.medium}</p></div></div>
            <div className="dashboard-empty"><BookOpen size={42} aria-hidden="true"/><h3>Coming Soon!</h3><p>Subjects and chapters for your curriculum will appear here when they are connected.</p></div>
          </section>
        </div>
        <footer className="dashboard-footer">© {new Date().getFullYear()} SchollyGo. All rights reserved.</footer>
      </main>
    </div>
    <nav className="dashboard-mobile-nav" aria-label="Mobile navigation">
      <span className="active" aria-current="page"><Tent size={23}/><small>Basecamp</small></span>
      <span className="disabled" aria-disabled="true"><BarChart3 size={23}/><small>Scorecard</small></span>
      <button type="button" onClick={onProfile}><CircleUserRound size={23}/><small>My Space</small></button>
    </nav>
  </div>;
}
