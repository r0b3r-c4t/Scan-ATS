import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import jobService from '../services/jobService'
import { JobCard } from '../components/CardComponents'
import { LoadingState, ErrorState, EmptyState } from '../components/StateComponents'
import './JobList.css'

const JobList = () => {
  const navigate = useNavigate()
  const [jobs, setJobs] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    loadJobs()
  }, [])

  const loadJobs = async () => {
    try {
      setLoading(true)
      setError(null)
      const data = await jobService.getJobs()
      setJobs(data)
    } catch (err) {
      console.error('Error loading jobs:', err)
      setError('Failed to load jobs')
    } finally {
      setLoading(false)
    }
  }

  if (error) {
    return <ErrorState message={error} onRetry={loadJobs} />
  }

  return (
    <div className="job-list-page">
      <div className="page-header">
        <div className="header-title">
          <h1>Jobs</h1>
          <p>Manage your open positions</p>
        </div>
        <button 
          className="btn btn-primary"
          onClick={() => navigate('/jobs/new')}
        >
          + Create Job
        </button>
      </div>

      {loading ? (
        <LoadingState message="Loading jobs..." />
      ) : jobs.length > 0 ? (
        <div className="jobs-grid">
          {jobs.map(job => (
            <JobCard 
              key={job._id || job.id} 
              job={job}
            />
          ))}
        </div>
      ) : (
        <EmptyState 
          message="No jobs created yet. Create your first job to start matching candidates."
          icon="💼"
          actionLabel="Create Job"
          onAction={() => navigate('/jobs/new')}
        />
      )}
    </div>
  )
}

export default JobList
