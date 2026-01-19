import numpy as np

def log_distance_path_loss(distance, d0, pl_d0, n, sigma):
    """
    Implements: PL(d) = PL(d0) + 10 * n * log10(d/d0) + Xsigma [cite: 11]
    """
    if distance <= 0:
        return 0
    
    # Path loss formula [cite: 11]
    path_loss = pl_d0 + 10 * n * np.log10(distance / d0)
    
    # Shadowing (Xsigma) [cite: 14]
    if sigma > 0:
        shadowing = np.random.normal(0, sigma)
        path_loss += shadowing
        
    return path_loss
