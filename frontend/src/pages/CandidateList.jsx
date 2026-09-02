import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import candidateService from '../services/candidateService'
import { CandidateCard } from '../components/CardComponents'
import { LoadingState, ErrorState, EmptyState } from '../components/StateComponents'
import './CandidateList.css'

const CandidateList = () => {
  const navigate = useNavigate()
  const [candidates, setCandidates] = useState([])
  const [filteredCandidates, setFilteredCandidates] = useState([])
  const [searchTerm, setSearchTerm] = useState('')
  const [sortBy, setSortBy] = useState('score')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    loadCandidates()
  }, [])

  useEffect(() => {
    filterAndSort()
  }, [candidates, searchTerm, sortBy])

  const loadCandidates = async () => {
    try {
      setLoading(true)
      setError(null)
      const data = await candidateService.getCandidates()
      setCandidates(data)
    } catch (err) {
      console.error('Error loading candidates:', err)
      setError('Failed to load candidates')
    } finally {
      setLoading(false)
    }
  }

  const filterAndSort = () => {
    let filtered = candidates.filter(candidate =>
      candidate.name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
      candidate.email?.toLowerCase().includes(searchTerm.toLowerCase())
    )

    filtered.sort((a, b) => {
      if (sortBy === 'score') {
        return (b.candidate_score || 0) - (a.candidate_score || 0)
      } else if (sortBy === 'name') {
        return (a.name || '').localeCompare(b.name || '')
      }
      return 0
    })

    setFilteredCandidates(filtered)
  }

  if (error) {
    return <ErrorState message={error} onRetry={loadCandidates} />
  }

  return (
    <div className="candidate-list-page">
      <div className="page-header">
        <div className="header-title">
          <h1>Candidates</h1>
          <p>Manage and evaluate your candidates</p>
        </div>
        <button 
          className="btn btn-primary"
          onClick={() => navigate('/candidates/upload')}
        >
          + Upload Resume
        </button>
      </div>

      <div className="candidate-filters">
        <input
          type="text"
          placeholder="Search candidates..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="search-input"
        />

        <select 
          value={sortBy} 
          onChange={(e) => setSortBy(e.target.value)}
          className="sort-select"
        >
          <option value="score">Sort by Score</option>
          <option value="name">Sort by Name</option>
        </select>
      </div>

      {loading ? (
        <LoadingState message="Loading candidates..." />
      ) : filteredCandidates.length > 0 ? (
        <div className="candidates-grid">
          {filteredCandidates.map(candidate => (
            <CandidateCard 
              key={candidate._id || candidate.id} 
              candidate={candidate}
            />
          ))}
        </div>
      ) : (
        <EmptyState 
          message={candidates.length === 0 
            ? "No candidates yet. Start by uploading a resume."
            : "No candidates match your search."
          }
          icon={candidates.length === 0 ? "📭" : "🔍"}
          actionLabel={candidates.length === 0 ? "Upload Resume" : undefined}
          onAction={candidates.length === 0 ? () => navigate('/candidates/upload') : undefined}
        />
      )}
    </div>
  )
}

export default CandidateList
