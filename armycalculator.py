import sqlite3
from collections import Counter

def create_connection(db_file="game_data.db"):
    """Create a database connection to the SQLite database"""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)
    
    return conn

def get_all_units(conn):
    """Get all units from the database ordered by metal value"""
    sql = "SELECT name, metal FROM units ORDER BY metal"
    
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(e)
        return []

def find_best_combination(units, max_metal):
    """Find the best combination using the fewest units possible"""
    # We'll use a greedy approach with the largest units first
    units_by_metal = sorted(units, key=lambda x: x[1], reverse=True)
    
    best_combo = None
    best_unit_count = float('inf')
    best_remaining = float('inf')
    
    # Try starting with each unit as the base
    for i, (unit_name, unit_metal) in enumerate(units_by_metal):
        if unit_metal > max_metal:
            continue
            
        combo = []
        remaining = max_metal
        
        # Use as many of the current unit as possible
        while remaining >= unit_metal:
            combo.append(unit_name)
            remaining -= unit_metal
            
        # If we have remaining metal, try to use the smallest unit
        if remaining > 0 and i < len(units_by_metal) - 1:
            # Find the smallest unit we can afford
            for small_unit, small_metal in reversed(units_by_metal):
                if small_metal <= remaining:
                    combo.append(small_unit)
                    remaining -= small_metal
                    break
        
        # Check if this combo is better
        if len(combo) < best_unit_count or (len(combo) == best_unit_count and remaining < best_remaining):
            best_combo = combo
            best_unit_count = len(combo)
            best_remaining = remaining
            
    return best_combo, best_remaining
def main():
    conn = create_connection()
    
    if conn is not None:
        try:
            user_metal = int(input("Enter the amount of metal you have: "))
            all_units = get_all_units(conn)
            
            if not all_units:
                print("No units found in the database!")
                return
            
            best_combo, remaining = find_best_combination(all_units, user_metal)
            
            if best_combo:
                print("\nBest combination of units:")
                unit_counts = Counter(best_combo)
                
                # Create a dictionary mapping unit names to their metal values
                unit_metal_map = {name: metal for name, metal in all_units}
                
                # Sort units by their metal value (descending)
                for unit, count in sorted(unit_counts.items(), 
                                         key=lambda x: unit_metal_map[x[0]], 
                                         reverse=True):
                    print(f"{count} {unit}")
                
                print(f"\nTotal units: {len(best_combo)}")
                print(f"Remaining metal: {remaining}")
                print(f"Total metal used: {user_metal - remaining}")
            else:
                print(f"Couldn't find any combination with metal <= {user_metal}")
        except ValueError:
            print("Please enter a valid number for metal value")
        finally:
            conn.close()
    else:
        print("Error! Cannot create the database connection.")
if __name__ == "__main__":
    main()