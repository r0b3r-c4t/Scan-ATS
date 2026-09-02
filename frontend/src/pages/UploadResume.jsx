import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import candidateService from '../services/candidateService'
import { LoadingState, ErrorState } from '../components/StateComponents'
import './UploadResume.css'

const UploadResume = () => {
  const navigate = useNavigate()
  const [file, setFile] = useState(null)
  const [loading, setLoading] = useState(false)
  const [uploadStatus, setUploadStatus] = useState(null)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0]
    if (selectedFile) {
      setFile(selectedFile)
      setUploadStatus(null)
      setError(null)
    }
  }

  const handleDrop = (e) => {
    e.preventDefault()
    const droppedFile = e.dataTransfer.files[0]
    if (droppedFile) {
      setFile(droppedFile)
      setUploadStatus(null)
      setError(null)
    }
  }

  const handleUpload = async () => {
    if (!file) {
      setError('Please select a file')
      return
    }

    try {
      setLoading(true)
      setError(null)
      setUploadStatus('Uploading...')

      setTimeout(() => setUploadStatus('Processing document...'), 500)
      setTimeout(() => setUploadStatus('Analyzing resume with AI...'), 1500)
      setTimeout(() => setUploadStatus('Calculating candidate score...'), 2500)
      setTimeout(() => setUploadStatus('Saving candidate...'), 3500)

      const response = await candidateService.uploadResume(file)
      
      setLoading(false)
      setResult(response)
      setUploadStatus('Resume analyzed successfully')
      setFile(null)
    } catch (err) {
      console.error('Error uploading resume:', err)
      setLoading(false)
      setError(err.response?.data?.detail || 'Failed to upload resume')
      setUploadStatus(null)
    }
  }

  if (result) {
    const candidateScore = result.candidate?.candidate_score?.score || result.candidate?.candidate_score || 0
    return (
      <div className="upload-success">
        <div className="success-icon">✓</div>
        <h2>Resume analyzed successfully</h2>
        
        <div className="success-score">
          <div className="score-ring-display">
            <div className="score-value">{Math.round(candidateScore)}</div>
            <div className="score-max">/ 100</div>
          </div>
          <div className="candidate-name">{result.candidate?.name}</div>
        </div>

        <div className="success-actions">
          <button 
            className="btn btn-primary"
            onClick={() => navigate(`/candidates/${result.candidate_id}`)}
          >
            View Candidate Profile
          </button>
          <button 
            className="btn btn-secondary"
            onClick={() => {
              setResult(null)
              setUploadStatus(null)
            }}
          >
            Upload Another Resume
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="upload-resume-page">
      <div className="upload-container">
        <h1>Upload Resume</h1>
        <p>Upload a PDF, JPG, or PNG file to analyze the candidate</p>

        {error && (
          <ErrorState message={error} onRetry={() => setError(null)} />
        )}

        {!error && (
          <>
            <div 
              className="upload-area"
              onDrop={handleDrop}
              onDragOver={(e) => e.preventDefault()}
            >
              <div className="upload-content">
                <div className="upload-icon">📄</div>
                <h3>Drag & Drop Resume</h3>
                <p>or</p>
                <label htmlFor="file-input" className="file-label">
                  Select File
                </label>
                <input
                  id="file-input"
                  type="file"
                  onChange={handleFileChange}
                  accept=".pdf,.jpg,.jpeg,.png"
                  style={{ display: 'none' }}
                />
                <p className="supported-formats">PDF / JPG / PNG</p>
              </div>
              
              {file && (
                <div className="file-selected">
                  <p>📎 {file.name}</p>
                  <p className="file-size">({(file.size / 1024).toFixed(2)} KB)</p>
                </div>
              )}
            </div>

            {loading && uploadStatus ? (
              <div className="upload-progress">
                <LoadingState message={uploadStatus} />
              </div>
            ) : (
              <button 
                className="btn btn-primary btn-large"
                onClick={handleUpload}
                disabled={!file || loading}
              >
                {loading ? 'Analyzing...' : 'Analyze Resume'}
              </button>
            )}
          </>
        )}
      </div>
    </div>
  )
}

export default UploadResume
