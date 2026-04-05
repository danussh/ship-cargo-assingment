# Web UI Guide - ShipIQ Cargo Optimization

## 🎨 Overview

The ShipIQ Web UI provides an intuitive, visual interface for cargo optimization. No coding required - just input your data and see the results instantly.

## 🚀 Quick Start

1. **Start the server**:
   ```bash
   python -m app.main
   ```

2. **Open in browser**:
   ```
   http://localhost:8000
   ```

3. **You're ready!** The UI will automatically load.

## 📋 Using the Interface

### Step 1: Input Your Data

#### Add Cargos
- Click **"+ Add Cargo"** to add more cargo rows
- Enter **Cargo ID** (e.g., C1, C2, C3)
- Enter **Volume** (positive number)
- Click **×** to remove a cargo

#### Add Tanks
- Click **"+ Add Tank"** to add more tank rows
- Enter **Tank ID** (e.g., T1, T2, T3)
- Enter **Capacity** (positive number)
- Click **×** to remove a tank

### Step 2: Quick Actions

- **Load Sample Data**: Loads the 10 cargos and 10 tanks from the assignment
- **Clear All**: Resets all inputs to start fresh

### Step 3: Optimize

Click the **"🚀 Optimize Allocation"** button to run the optimization algorithm.

### Step 4: View Results

The results section displays:

#### 📊 Metrics Cards (6 Key Indicators)
1. **Total Cargo Volume** - Sum of all cargo volumes
2. **Total Tank Capacity** - Sum of all tank capacities
3. **Total Loaded** - How much cargo was successfully allocated
4. **Tank Utilization** - Percentage of tank capacity used
5. **Cargo Loaded** - Percentage of cargo successfully allocated
6. **Tanks Used** - Number of tanks with cargo / total tanks

#### 🎨 Tank Visualization
- **Color-coded bar charts** for each tank
- Each cargo gets a unique color
- Bar height shows utilization percentage
- Hover to see details

#### 📋 Detailed Allocations Table
Shows every allocation with:
- Tank ID
- Cargo ID
- Volume allocated
- Tank capacity
- Utilization percentage

#### ⚠️ Unallocated Cargo (if any)
- Lists cargo that couldn't be fully allocated
- Shows how much volume remains unallocated
- Percentage of original cargo volume

## 🎯 Example Workflow

### Scenario: Simple Optimization

1. **Input**:
   - Cargo C1: 1234 cubic units
   - Cargo C2: 4352 cubic units
   - Tank T1: 5000 cubic units
   - Tank T2: 3000 cubic units

2. **Click**: "🚀 Optimize Allocation"

3. **Results**:
   - Total Loaded: 5586 units
   - Tank Utilization: ~70%
   - C2 goes to T1 (4352 units)
   - C1 goes to T2 (1234 units)

### Scenario: Using Sample Data

1. **Click**: "Load Sample Data"
   - Automatically loads 10 cargos and 10 tanks

2. **Click**: "🚀 Optimize Allocation"

3. **View**:
   - 34,512 total cargo volume
   - 40,000 total tank capacity
   - ~86% tank utilization
   - Visual breakdown of all allocations

## 🎨 Visual Features

### Color Coding
Each cargo is assigned a unique color:
- **Blue** (#2563eb)
- **Green** (#10b981)
- **Orange** (#f59e0b)
- **Red** (#ef4444)
- **Purple** (#8b5cf6)
- **Pink** (#ec4899)
- **Cyan** (#06b6d4)
- **Lime** (#84cc16)
- And more...

### Tank Bars
- **Height**: Represents utilization percentage
- **Color**: Matches the cargo color
- **Label**: Shows percentage if space allows
- **Info**: Displays cargo ID and volume below

### Responsive Design
- Works on desktop, tablet, and mobile
- Adapts layout for smaller screens
- Touch-friendly buttons

## 🔧 Tips & Tricks

### Best Practices
1. **Start with sample data** to understand the interface
2. **Use meaningful IDs** (C1, C2 vs random strings)
3. **Check unallocated cargo** to see what didn't fit
4. **Experiment** with different tank sizes to improve utilization

### Common Scenarios

**All cargo fits perfectly**:
- Cargo Loaded: 100%
- No unallocated cargo section

**Some cargo doesn't fit**:
- Cargo Loaded: <100%
- Unallocated section appears with details

**Poor utilization**:
- Tank Utilization: Low percentage
- Consider adding more tanks or adjusting sizes

### Validation
The UI validates:
- ✅ At least one cargo and one tank required
- ✅ All volumes/capacities must be positive
- ✅ IDs cannot be empty
- ❌ Duplicate IDs are allowed (handled by backend)

## 🐛 Troubleshooting

### Error: "Please add at least one cargo and one tank"
- **Cause**: Empty cargo or tank list
- **Fix**: Add at least one valid entry for each

### Error: "Optimization failed"
- **Cause**: Invalid input data (negative values, etc.)
- **Fix**: Check all inputs are positive numbers

### Server not responding
- **Cause**: Backend not running
- **Fix**: Start the server with `python -m app.main`

### UI not loading
- **Cause**: Wrong URL or port
- **Fix**: Ensure you're accessing http://localhost:8000

## 📱 Mobile Usage

The UI is fully responsive:
- Input fields stack vertically
- Metrics cards stack in single column
- Tank visualizations wrap naturally
- Touch-friendly buttons and inputs

## 🎓 Understanding the Results

### Tank Utilization vs Cargo Loaded

**Tank Utilization**: How efficiently are we using available tank space?
- 100% = All tanks are full
- 50% = Half of total tank capacity is used

**Cargo Loaded**: How much of the cargo did we successfully allocate?
- 100% = All cargo is allocated
- 50% = Half of the cargo couldn't fit

### Ideal Scenario
- Tank Utilization: High (>80%)
- Cargo Loaded: 100%
- Tanks Used: As few as possible (efficient packing)

### Optimization Needed
- Tank Utilization: Low (<50%)
- Cargo Loaded: Low (<80%)
- Many unallocated cargos

## 🔗 Integration

The UI uses the REST API endpoints:
- `POST /api/v1/optimize` - Main optimization endpoint
- Sends JSON with cargos and tanks
- Receives detailed results

You can also use:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **cURL**: Command-line testing
- **Postman**: API testing tool

## 🎉 Features Showcase

### Dynamic Input Management
- Add unlimited cargos and tanks
- Remove any row instantly
- No page refresh needed

### Real-time Feedback
- Loading spinner during optimization
- Error messages for invalid input
- Success indicators

### Professional Design
- Modern gradient headers
- Smooth animations
- Card-based layout
- Consistent color scheme

### Accessibility
- Clear labels and placeholders
- High contrast colors
- Keyboard navigation support
- Responsive touch targets

---

**Enjoy optimizing your cargo allocations! 🚢**
