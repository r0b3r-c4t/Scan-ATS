import React from 'react'
import './StateComponents.css'

export const LoadingState = ({ message = 'Loading...' }) => {
  return (
    <div className="loading-state">
      <div className="loading-spinner"></div>
      <p>{message}</p>
    </div>
  )
}

export const ErrorState = ({ message = 'Something went wrong', onRetry = null }) => {
  return (
    <div className="error-state">
      <div className="error-icon">⚠️</div>
      <p>{message}</p>
      {onRetry && (
        <button className="btn btn-primary" onClick={onRetry}>
          Retry
        </button>
      )}
    </div>
  )
}

export const EmptyState = ({ message = 'No data available', icon = '📭', actionLabel = null, onAction = null }) => {
  return (
    <div className="empty-state">
      <div className="empty-icon">{icon}</div>
      <p>{message}</p>
      {actionLabel && onAction && (
        <button className="btn btn-primary" onClick={onAction}>
          {actionLabel}
        </button>
      )}
    </div>
  )
}

export default { LoadingState, ErrorState, EmptyState }
