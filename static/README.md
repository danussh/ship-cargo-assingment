# ShipIQ Cargo Optimization - Web UI

A modern, interactive web interface for visualizing cargo-to-tank allocation optimization.

## Features

- 📊 **Interactive Input** - Add/remove cargos and tanks dynamically
- 🎨 **Visual Tank Display** - Color-coded bar charts showing tank utilization
- 📈 **Real-time Metrics** - Total volumes, utilization percentages, and efficiency stats
- 📋 **Detailed Tables** - Complete allocation breakdown
- ⚠️ **Unallocated Tracking** - Highlights cargo that couldn't be allocated
- 🚀 **Sample Data** - One-click loading of assignment sample data
- 📱 **Responsive Design** - Works on desktop, tablet, and mobile

## How to Use

1. **Start the server** (if not already running):
   ```bash
   python -m app.main
   ```

2. **Open in browser**:
   - Go to: http://localhost:8000
   - Or directly: http://localhost:8000/static/index.html

3. **Add your data**:
   - Enter cargo IDs and volumes
   - Enter tank IDs and capacities
   - Or click "Load Sample Data" for quick testing

4. **Optimize**:
   - Click "🚀 Optimize Allocation"
   - View results with visual tank charts
   - See detailed metrics and allocations

## UI Components

### Input Section
- Dynamic cargo/tank input rows
- Add/remove functionality
- Sample data loader
- Clear all button

### Results Section
- **Metrics Cards**: 6 key performance indicators
- **Tank Visualization**: Color-coded bar charts for each tank
- **Allocations Table**: Detailed breakdown of all allocations
- **Unallocated Cargo**: Warning section for cargo that couldn't fit

## Technology Stack

- **Pure JavaScript** - No frameworks, lightweight and fast
- **Modern CSS** - Flexbox, Grid, gradients, animations
- **Responsive Design** - Mobile-first approach
- **FastAPI Backend** - RESTful API integration

## Color Coding

Each cargo is assigned a unique color for easy visual identification across tanks:
- Blue, Green, Orange, Red, Purple, Pink, Cyan, Lime, etc.

## Browser Support

- Chrome/Edge (recommended)
- Firefox
- Safari
- Opera

---

**Built with ❤️ for ShipIQ**
