import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import candidateService from '../services/candidateService'
import jobService from '../services/jobService'
import { ScoreCard } from '../components/ScoreRing'
import { LoadingState, ErrorState, EmptyState } from '../components/StateComponents'
import './Dashboard.css'

const Dashboard = () => {
  const [stats, setStats] = useState({
    totalCandidates: 0,
    totalJobs: 0,
    avgCandidateScore: 0,
    avgMatchScore: 0
  })
  const [topCandidates, setTopCandidates] = useState([])
  const [recentCandidates, setRecentCandidates] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    loadDashboardData()
  }, [])

  const loadDashboardData = async () => {
    try {
      setLoading(true)
      setError(null)

      const [candidates, jobs] = await Promise.all([
        candidateService.getCandidates(),
        jobService.getJobs()
      ])

      setStats({
        totalCandidates: candidates.length,
        totalJobs: jobs.length,
        avgCandidateScore: candidates.length > 0
          ? Math.round(candidates.reduce((sum, c) => sum + (c.candidate_score || 0), 0) / candidates.length)
          : 0,
        avgMatchScore: 0
      })

      const sorted = [...candidates].sort((a, b) => 
        (b.candidate_score || 0) - (a.candidate_score || 0)
      )

      setTopCandidates(sorted.slice(0, 5))
      setRecentCandidates(sorted.slice(0, 5).reverse())
    } catch (err) {
      console.error('Error loading dashboard:', err)
      setError('Failed to load dashboard data')
    } finally {
      setLoading(false)
    }
  }

  if (error) {
    return <ErrorState message={error} onRetry={loadDashboardData} />
  }

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h1>Dashboard</h1>
        <p>Talent overview and recruitment insights</p>
      </div>

      {loading ? (
        <LoadingState message="Loading dashboard..." />
      ) : (
        <>
          {/* Stats Cards */}
          <div className="stats-grid">
            <div className="stat-card">
              <div className="stat-label">Total Candidates</div>
              <div className="stat-value">{stats.totalCandidates}</div>
            </div>
            <div className="stat-card">
              <div className="stat-label">Total Jobs</div>
              <div className="stat-value">{stats.totalJobs}</div>
            </div>
            <div className="stat-card">
              <div className="stat-label">Avg Candidate Score</div>
              <div className="stat-value">{stats.avgCandidateScore}</div>
            </div>
            <div className="stat-card">
              <div className="stat-label">Avg Match Score</div>
              <div className="stat-value">{stats.avgMatchScore}</div>
            </div>
          </div>

          {/* Top Candidates */}
          <div className="dashboard-section">
            <div className="section-header">
              <h2>Top Candidates</h2>
              <Link to="/candidates" className="link-view-all">View All →</Link>
            </div>

            {topCandidates.length > 0 ? (
              <div className="candidates-list">
                {topCandidates.map(candidate => (
                  <Link
                    key={candidate._id || candidate.id}
                    to={`/candidates/${candidate._id || candidate.id}`}
                    className="candidate-item"
                  >
                    <span className="candidate-name">{candidate.name}</span>
                    <span className="candidate-score">
                      {Math.round(candidate.candidate_score || 0)}
                    </span>
                  </Link>
                ))}
              </div>
            ) : (
              <EmptyState message="No candidates yet" />
            )}
          </div>

          {/* Recent Candidates */}
          <div className="dashboard-section">
            <div className="section-header">
              <h2>Recent Candidates</h2>
              <Link to="/candidates/upload" className="link-view-all">Upload Resume →</Link>
            </div>

            {recentCandidates.length > 0 ? (
              <div className="candidates-list">
                {recentCandidates.map(candidate => (
                  <Link
                    key={candidate._id || candidate.id}
                    to={`/candidates/${candidate._id || candidate.id}`}
                    className="candidate-item"
                  >
                    <span className="candidate-name">{candidate.name}</span>
                    <span className="candidate-score">
                      {Math.round(candidate.candidate_score || 0)}
                    </span>
                  </Link>
                ))}
              </div>
            ) : (
              <EmptyState message="No recent candidates" />
            )}
          </div>
        </>
      )}
    </div>
  )
}

export default Dashboard
