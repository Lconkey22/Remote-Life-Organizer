import os
if not os.path.exists('backend'):
    os.makedirs('backend')
if not os.path.exists('backend/routers'):
    os.makedirs('backend/routers')

# Create __init__.py files to make them proper Python packages
with open('backend/__init__.py', 'w') as f:
    pass
with open('backend/routers/__init__.py', 'w') as f:
    pass

