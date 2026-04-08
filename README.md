# ARI711S – Artificial Intelligence Group Project 2026

**Qualification:** Bachelor of Computer Science (Software Development)  
**Course:** Artificial Intelligence – ARI711S  
**Assessment:** Group Project  
**Due Date:** 30 April 2026  

## Group Members
- Tangi
- Matias
- Aguero
- Meke
- Trizzy

---

## Project Structure

```
├── part1/          # Search Algorithms – Flight Connections
├── part2/          # Optimization – Hospital Shift Scheduler
└── part3/          # Machine Learning – Traffic Sign Recognition
```

---

## Part 1: Flight Connections Search

Finds the shortest flight path between two cities using Breadth-First Search (BFS).

### How to run
```bash
cd part1
python3 flights.py data
```
Enter two city names when prompted. The program returns the shortest sequence of flights connecting them.

### Files
- `flights.py` – Main program with BFS search, Node, QueueFrontier, and StackFrontier classes
- `test_flights.py` – Unit tests
- `data/` – CSV dataset files (cities.csv, flights.csv, airlines.csv)

---

## Part 2: Hospital Shift Scheduler

Solves nurse weekly scheduling as a Constraint Satisfaction Problem (CSP) using AC-3 arc consistency and backtracking search with the MRV heuristic.

### How to run
```bash
cd part2
python3 scheduler.py staff_small.txt
python3 scheduler.py staff_medium.txt
python3 scheduler.py staff_complex.txt
```

### Files
- `shift_solver.py` – `Shift_AI_Solver` class with node consistency, AC-3, MRV, and backtracking
- `scheduler.py` – Main runner that loads staff files and displays the schedule
- `test_scheduler.py` – Unit tests
- `staff_small.txt`, `staff_medium.txt`, `staff_complex.txt` – Staff datasets

---

## Part 3: Traffic Sign Recognition

Trains a Convolutional Neural Network (CNN) using TensorFlow to classify 43 categories of German traffic signs from the GTSRB dataset.

### Dependencies
```bash
pip install tensorflow opencv-python scikit-learn numpy
```

### How to run
```bash
cd part3
python3 traffic.py gtsrb model.h5
```

Place the unzipped `gtsrb/` folder (43 subfolders named 0–42) in the `part3/` directory before running.

### Files
- `traffic.py` – Full CNN pipeline: data loading, model building, training, evaluation, and saving

---

## License
MIT License – see LICENSE file for details.
