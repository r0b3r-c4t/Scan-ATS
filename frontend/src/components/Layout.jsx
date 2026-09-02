import React from 'react'
import { Link, useLocation } from 'react-router-dom'
import './Layout.css'

export const Layout = ({ children }) => {
  const [sidebarOpen, setSidebarOpen] = React.useState(true)
  const location = useLocation()

  const isActive = (path) => {
    return location.pathname.startsWith(path) ? 'active' : ''
  }

  return (
    <div className="layout">
      <aside className={`sidebar ${sidebarOpen ? 'open' : 'closed'}`}>
        <div className="sidebar-header">
          <Link to="/" className="logo">
            <span className="logo-icon">📊</span>
            <span className="logo-text">Scan-ATS</span>
          </Link>
          <button 
            className="sidebar-toggle"
            onClick={() => setSidebarOpen(!sidebarOpen)}
            title={sidebarOpen ? 'Close sidebar' : 'Open sidebar'}
          >
            {sidebarOpen ? '←' : '→'}
          </button>
        </div>

        <nav className="sidebar-nav">
          <Link 
            to="/dashboard" 
            className={`nav-link ${isActive('/dashboard')}`}
          >
            <span className="nav-icon">📈</span>
            <span className="nav-label">Dashboard</span>
          </Link>

          <Link 
            to="/candidates" 
            className={`nav-link ${isActive('/candidates')}`}
          >
            <span className="nav-icon">👥</span>
            <span className="nav-label">Candidates</span>
          </Link>

          <Link 
            to="/jobs" 
            className={`nav-link ${isActive('/jobs')}`}
          >
            <span className="nav-icon">💼</span>
            <span className="nav-label">Jobs</span>
          </Link>

          <Link 
            to="/matches" 
            className={`nav-link ${isActive('/matches')}`}
          >
            <span className="nav-icon">🎯</span>
            <span className="nav-label">Matches</span>
          </Link>
        </nav>

        <div className="sidebar-footer">
          <Link 
            to="/settings" 
            className={`nav-link ${isActive('/settings')}`}
          >
            <span className="nav-icon">⚙️</span>
            <span className="nav-label">Settings</span>
          </Link>
        </div>
      </aside>

      <main className="main-content">
        <header className="header">
          <div className="header-content">
            <button 
              className="mobile-toggle"
              onClick={() => setSidebarOpen(!sidebarOpen)}
            >
              ☰
            </button>
            <h1 className="page-title"></h1>
            <div className="header-actions">
              <span className="user-badge">👤 User</span>
            </div>
          </div>
        </header>

        <div className="content-area">
          {children}
        </div>
      </main>
    </div>
  )
}

export default Layout
