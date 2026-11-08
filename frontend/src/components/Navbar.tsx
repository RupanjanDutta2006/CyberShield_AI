import React from 'react';
import { NavLink, Link } from 'react-router-dom';
import { Shield, Search, MessageSquare, History, Settings, Activity, Sparkles } from 'lucide-react';

export const Navbar: React.FC = () => {
  const navItems = [
    { name: 'Research Hub', path: '/', icon: Sparkles, highlight: true },
    { name: 'Dashboard', path: '/dashboard', icon: Activity },
    { name: 'URL Scanner', path: '/scanner', icon: Search },
    { name: 'Message Analyzer', path: '/message-analyzer', icon: MessageSquare },
    { name: 'Scan History', path: '/history', icon: History },
    { name: 'System & APIs', path: '/settings', icon: Settings },
  ];

  return (
    <header className="sticky top-0 z-50 backdrop-blur-md bg-black/90 border-b border-[#2A2A2A]">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16 font-mono">
          {/* Logo & Branding */}
          <Link to="/" className="flex items-center gap-3 group">
            <div className="w-10 h-10 rounded-lg border border-[#2A2A2A] bg-[#111111] flex items-center justify-center shadow-lg shadow-[#AA88FF]/10 group-hover:border-[#AA88FF]/40 transition-all">
              <Shield className="w-5 h-5 text-[#AA88FF]" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="font-bold text-sm tracking-widest text-[#DDDDDD] group-hover:text-white transition-colors uppercase">
                  CyberShield AI
                </span>
                <span className="px-1.5 py-0.5 text-[9px] font-bold uppercase tracking-wider rounded bg-[#AA88FF]/15 text-[#AA88FF] border border-[#AA88FF]/30">
                  GPU v2.0
                </span>
              </div>
              <p className="text-[10px] text-[#8A8A8A] font-medium hidden sm:block uppercase">
                Digital Threat Intelligence
              </p>
            </div>
          </Link>

          {/* Navigation Links */}
          <nav className="flex items-center gap-1 sm:gap-2">
            {navItems.map((item) => {
              const Icon = item.icon;
              return (
                <NavLink
                  key={item.path}
                  to={item.path}
                  end={item.path === '/'}
                  className={({ isActive }) =>
                    `flex items-center gap-2 px-3 py-1.5 rounded-lg text-xs font-medium uppercase tracking-wider transition-all ${
                      isActive
                        ? item.highlight
                          ? 'bg-[#AA88FF]/20 text-[#AA88FF] border border-[#AA88FF]/40 shadow-sm shadow-[#AA88FF]/20'
                          : 'bg-[#1C1C1C] text-white border border-[#333333]'
                        : item.highlight
                        ? 'text-[#AA88FF]/90 hover:text-[#AA88FF] hover:bg-[#AA88FF]/10 border border-[#AA88FF]/20'
                        : 'text-[#8A8A8A] hover:text-[#DDDDDD] hover:bg-[#181818] border border-transparent'
                    }`
                  }
                >
                  <Icon className="w-3.5 h-3.5" />
                  <span className="hidden md:inline">{item.name}</span>
                </NavLink>
              );
            })}
          </nav>

          {/* Engine Status Indicator */}
          <div className="hidden lg:flex items-center gap-3 border-l border-[#2A2A2A] pl-4">
            <div className="flex items-center gap-2 px-3 py-1 rounded-full bg-[#1C1C1C] border border-[#2A2A2A]">
              <span className="w-2 h-2 rounded-full bg-emerald-400 animate-ping" />
              <span className="text-[11px] font-medium text-[#DDDDDD] uppercase">GPU Grid Active</span>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
};
