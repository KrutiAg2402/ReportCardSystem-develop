# ============================================================================
# IMPORTS: Database connection and utility functions
# ============================================================================
# - get_connection: Establishes MySQL database connection
# - calculate_grade: Converts percentage scores to letter grades
# - is_valid_marks: Validates that marks are within 0-100 range

from connection import get_connection
from utils import calculate_grade, is_valid_marks

# ============================================================================
# STUDENT INFORMATION CRUD OPERATIONS
# ============================================================================

def add_student():
    """Add new student to the Students table (Teacher only)"""
    conn = get_connection()
    cursor = conn.cursor()

    try:
        Student_Name = input("Enter Student Name: ").strip()
        Father_Name = input("Enter Father's Name: ").strip()
        Mother_Name = input("Enter Mother's Name: ").strip()
        Parent_Number = input("Enter Parent Phone Number: ").strip()
        Address = input("Enter Address: ").strip()

        query = """
        INSERT INTO Students (`Student_Name`, `Father_Name`, `Mother_Name`, `Parent_Number`, `Address`)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (Student_Name, Father_Name, Mother_Name, Parent_Number, Address))
        conn.commit()
        student_id = cursor.lastrowid
        print(f"✅ Student added successfully with UID: {student_id}")
    except Exception as e:
        print("❌ Error:", e)
    finally:
        conn.close()

# ============================================================================
# STUDENT MARKS CRUD OPERATIONS
# ============================================================================

def add_marks():
    """Add marks for a student (Teacher only)"""
    conn = get_connection()
    cursor = conn.cursor()

    try:
        UID = int(input("Enter Student UID: "))
        
        # Check if student exists
        cursor.execute("SELECT Student_Name FROM Students WHERE UID = %s", (UID,))
        student = cursor.fetchone()
        if not student:
            print("❌ Student not found.")
            conn.close()
            return

        print(f"Adding marks for: {student[0]}")
        Physics_Marks = int(input("Physics Marks (0-100): "))
        Chemistry_Marks = int(input("Chemistry Marks (0-100): "))
        Mathematics_Marks = int(input("Mathematics Marks (0-100): "))
        English_Marks = int(input("English Marks (0-100): "))
        Computer_Marks = int(input("Computer Marks (0-100): "))
        PHE_Marks = int(input("PHE Marks (0-100): "))

        if not all(map(is_valid_marks, [Physics_Marks, Chemistry_Marks, Mathematics_Marks, English_Marks, Computer_Marks, PHE_Marks])):
            print("❌ Invalid marks entered! Must be between 0 and 100.")
            conn.close()
            return

        total = Physics_Marks + Chemistry_Marks + Mathematics_Marks + English_Marks + Computer_Marks + PHE_Marks
        percentage = total / 6
        grade = calculate_grade(percentage)

        query = """
        INSERT INTO Student_Marks (`UID`, `Physics_Marks`, `Chemistry_Marks`, `Mathematics_Marks`, `English_Marks`, `Computer_Marks`, `PHE_Marks`, `Total`, `Percentage`, `Grade`)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (UID, Physics_Marks, Chemistry_Marks, Mathematics_Marks, English_Marks, Computer_Marks, PHE_Marks, total, percentage, grade))
        conn.commit()
        print("✅ Marks added successfully.")
    except ValueError:
        print("❌ Invalid input. Please enter valid numbers.")
    except Exception as e:
        print("❌ Error:", e)
    finally:
        conn.close()

def view_report(roll_no=None):
    """View student report card with information and marks in table format"""
    conn = get_connection()
    cursor = conn.cursor()

    try:
        if roll_no is None:
            roll_no = int(input("Enter Student UID: "))

        # Get student information
        cursor.execute("SELECT UID, Student_Name, Father_Name, Mother_Name, Parent_Number, Address FROM Students WHERE UID = %s", (roll_no,))
        student = cursor.fetchone()

        if not student:
            print("❌ Student not found.")
            conn.close()
            return

        # Get student marks
        cursor.execute("SELECT Physics_Marks, Chemistry_Marks, Mathematics_Marks, English_Marks, Computer_Marks, PHE_Marks, Total, Percentage, Grade FROM Student_Marks WHERE UID = %s ORDER BY Updated_At DESC LIMIT 1", (roll_no,))
        marks = cursor.fetchone()

        # Display header
        print("\n" + "="*100)
        print(" "*35 + "📋 STUDENT REPORT CARD")
        print("="*100)
        
        # Student Information Table
        print("\n📌 STUDENT INFORMATION")
        print("-"*100)
        print(f"{'UID':<15} {'Student Name':<25} {'Father Name':<20} {'Mother Name':<20} {'Parent Phone':<20}")
        print("-"*100)
        print(f"{student[0]:<15} {student[1]:<25} {student[2]:<20} {student[3]:<20} {student[4]:<20}")
        print("-"*100)
        print(f"{'Address:':<15} {student[5]:<85}")
        print("="*100)
        
        # Marks Table
        if marks:
            print("\n📚 ACADEMIC MARKS")
            print("-"*100)
            print(f"{'Subject':<20} {'Marks':<20} {'Subject':<20} {'Marks':<20} {'Subject':<20} {'Marks':<20}")
            print("-"*100)
            print(f"{'Physics':<20} {marks[0]:<20} {'Chemistry':<20} {marks[1]:<20} {'Mathematics':<20} {marks[2]:<20}")
            print(f"{'English':<20} {marks[3]:<20} {'Computer':<20} {marks[4]:<20} {'PHE':<20} {marks[5]:<20}")
            print("="*100)
            
            # Summary Table
            print("\n📊 SUMMARY")
            print("-"*100)
            print(f"{'Total Marks':<30} {'Percentage':<30} {'Grade':<30}")
            print("-"*100)
            print(f"{marks[6]:<30} {marks[7]:.2f}%{' ':<28} {marks[8]:<30}")
            print("="*100 + "\n")
        else:
            print("\n⚠️  No marks record found yet.")
            print("="*100 + "\n")
    except ValueError:
        print("❌ Invalid input.")
    except Exception as e:
        print("❌ Error:", e)
    finally:
        conn.close()

# ============================================================================
# STUDENT INFORMATION UPDATE/DELETE OPERATIONS
# ============================================================================

def update_student_info():
    """Update student information (Teacher only)"""
    conn = get_connection()
    cursor = conn.cursor()

    try:
        UID = int(input("Enter Student UID to Update: "))
        cursor.execute("SELECT * FROM Students WHERE UID = %s", (UID,))
        if not cursor.fetchone():
            print("❌ Student not found.")
            conn.close()
            return

        print("\nLeave field empty to keep current value:")
        Student_Name = input("Update Student Name: ").strip()
        Father_Name = input("Update Father's Name: ").strip()
        Mother_Name = input("Update Mother's Name: ").strip()
        Parent_Number = input("Update Parent Phone Number: ").strip()
        Address = input("Update Address: ").strip()

        updates = []
        params = []

        if Student_Name:
            updates.append("Student_Name = %s")
            params.append(Student_Name)
        if Father_Name:
            updates.append("Father_Name = %s")
            params.append(Father_Name)
        if Mother_Name:
            updates.append("Mother_Name = %s")
            params.append(Mother_Name)
        if Parent_Number:
            updates.append("Parent_Number = %s")
            params.append(Parent_Number)
        if Address:
            updates.append("Address = %s")
            params.append(Address)

        if not updates:
            print("⚠️  No changes made.")
            conn.close()
            return

        params.append(UID)
        query = f"UPDATE Students SET {', '.join(updates)} WHERE UID = %s"
        cursor.execute(query, params)
        conn.commit()
        print("✅ Student information updated.")
    except ValueError:
        print("❌ Invalid input.")
    except Exception as e:
        print("❌ Error:", e)
    finally:
        conn.close()

def update_marks():
    """Update student marks (Teacher only) - leave blank to skip updating a subject"""
    conn = get_connection()
    cursor = conn.cursor()

    try:
        UID = int(input("Enter Student UID to Update Marks: "))
        cursor.execute("SELECT Student_Name FROM Students WHERE UID = %s", (UID,))
        student = cursor.fetchone()
        if not student:
            print("❌ Student not found.")
            conn.close()
            return

        print(f"Updating marks for: {student[0]}")
        print("Leave field empty to keep current value:\n")
        
        # Get current marks first
        cursor.execute("SELECT Physics_Marks, Chemistry_Marks, Mathematics_Marks, English_Marks, Computer_Marks, PHE_Marks FROM Student_Marks WHERE UID = %s ORDER BY Updated_At DESC LIMIT 1", (UID,))
        current_marks = cursor.fetchone()
        
        # Input new marks
        physics_input = input("Update Physics Marks (0-100): ").strip()
        chemistry_input = input("Update Chemistry Marks (0-100): ").strip()
        mathematics_input = input("Update Mathematics Marks (0-100): ").strip()
        english_input = input("Update English Marks (0-100): ").strip()
        computer_input = input("Update Computer Marks (0-100): ").strip()
        phe_input = input("Update PHE Marks (0-100): ").strip()

        # Use current values if blank, otherwise use new values
        if current_marks:
            Physics_Marks = int(physics_input) if physics_input else current_marks[0]
            Chemistry_Marks = int(chemistry_input) if chemistry_input else current_marks[1]
            Mathematics_Marks = int(mathematics_input) if mathematics_input else current_marks[2]
            English_Marks = int(english_input) if english_input else current_marks[3]
            Computer_Marks = int(computer_input) if computer_input else current_marks[4]
            PHE_Marks = int(phe_input) if phe_input else current_marks[5]
        else:
            # If no current marks, all fields are required
            Physics_Marks = int(physics_input) if physics_input else 0
            Chemistry_Marks = int(chemistry_input) if chemistry_input else 0
            Mathematics_Marks = int(mathematics_input) if mathematics_input else 0
            English_Marks = int(english_input) if english_input else 0
            Computer_Marks = int(computer_input) if computer_input else 0
            PHE_Marks = int(phe_input) if phe_input else 0

        if not all(map(is_valid_marks, [Physics_Marks, Chemistry_Marks, Mathematics_Marks, English_Marks, Computer_Marks, PHE_Marks])):
            print("❌ Invalid marks entered! Must be between 0 and 100.")
            conn.close()
            return

        total = Physics_Marks + Chemistry_Marks + Mathematics_Marks + English_Marks + Computer_Marks + PHE_Marks
        percentage = total / 6
        grade = calculate_grade(percentage)

        # Get the latest Mark_ID for this student first (separate query to avoid MySQL subquery limitation)
        cursor.execute("SELECT Mark_ID FROM Student_Marks WHERE UID = %s ORDER BY Updated_At DESC LIMIT 1", (UID,))
        mark_record = cursor.fetchone()
        
        if mark_record:
            # Update the latest marks record for this student
            mark_id = mark_record[0]
            query = """
            UPDATE Student_Marks SET Physics_Marks=%s, Chemistry_Marks=%s, Mathematics_Marks=%s, 
            English_Marks=%s, Computer_Marks=%s, PHE_Marks=%s, Total=%s, Percentage=%s, Grade=%s 
            WHERE Mark_ID = %s
            """
            cursor.execute(query, (Physics_Marks, Chemistry_Marks, Mathematics_Marks, English_Marks, Computer_Marks, PHE_Marks, total, percentage, grade, mark_id))
            conn.commit()
            print("✅ Marks updated successfully.")
        else:
            print("⚠️  No marks record found. Adding new marks record...")
            query = """
            INSERT INTO Student_Marks (`UID`, `Physics_Marks`, `Chemistry_Marks`, `Mathematics_Marks`, `English_Marks`, `Computer_Marks`, `PHE_Marks`, `Total`, `Percentage`, `Grade`)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (UID, Physics_Marks, Chemistry_Marks, Mathematics_Marks, English_Marks, Computer_Marks, PHE_Marks, total, percentage, grade))
            conn.commit()
            print("✅ Marks added successfully.")
    except ValueError:
        print("❌ Invalid input. Please enter valid numbers.")
    except Exception as e:
        print("❌ Error:", e)
    finally:
        conn.close()

def delete_student():
    """Delete student and associated marks (Teacher only)"""
    conn = get_connection()
    cursor = conn.cursor()

    try:
        UID = int(input("Enter Student UID to Delete: "))
        cursor.execute("SELECT Student_Name FROM Students WHERE UID = %s", (UID,))
        student = cursor.fetchone()
        if not student:
            print("❌ Student not found.")
            conn.close()
            return

        confirm = input(f"Are you sure you want to delete {student[0]}? (yes/no): ").lower()
        if confirm != 'yes':
            print("❌ Deletion cancelled.")
            conn.close()
            return

        # Marks will be deleted automatically due to CASCADE constraint
        cursor.execute("DELETE FROM Students WHERE UID = %s", (UID,))
        conn.commit()
        print("🗑️  Student record deleted successfully.")
    except ValueError:
        print("❌ Invalid input.")
    except Exception as e:
        print("❌ Error:", e)
    finally:
        conn.close()

def list_all_students():
    """List all students (Teacher only)"""
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT UID, Student_Name, Father_Name, Parent_Number FROM Students ORDER BY UID")
        students = cursor.fetchall()

        if not students:
            print("⚠️  No students found.")
            conn.close()
            return

        print("\n" + "="*70)
        print(f"{'UID':<8} {'Student Name':<25} {'Father Name':<20} {'Phone':<15}")
        print("="*70)
        for student in students:
            print(f"{student[0]:<8} {student[1]:<25} {student[2]:<20} {student[3]:<15}")
        print("="*70 + "\n")
    except Exception as e:
        print("❌ Error:", e)
    finally:
        conn.close()

# ============================================================================
# MENU OPERATIONS
# ============================================================================

def teacher_menu():
    """Teacher menu with full CRUD operations"""
    while True:
        print("\n📘 Teacher Menu")
        print("1. Add Student (Information)")
        print("2. Add Marks for Student")
        print("3. View Student Report")
        print("4. Update Student Information")
        print("5. Update Student Marks")
        print("6. List All Students")
        print("7. Delete Student")
        print("8. Exit")

        choice = input("Enter your choice (1-8): ").strip()

        if choice == '1':
            add_student()
        elif choice == '2':
            add_marks()
        elif choice == '3':
            view_report()
        elif choice == '4':
            update_student_info()
        elif choice == '5':
            update_marks()
        elif choice == '6':
            list_all_students()
        elif choice == '7':
            delete_student()
        elif choice == '8':
            print("👋 Exiting Teacher Menu...\n")
            break
        else:
            print("❌ Invalid choice. Please try again.")

def student_menu():
    """Student menu - view only access"""
    try:
        roll_no = int(input("Enter Your Roll Number (UID): "))
        view_report(roll_no)
    except ValueError:
        print("❌ Invalid input. Please enter a valid number.")

def main():
    """Main application entry point"""
    print("="*50)
    print("🎓 Student Report Card System")
    print("="*50)
    
    while True:
        print("\nSelect Role:")
        print("1. Teacher (Full Access)")
        print("2. Student (View Only)")
        print("3. Exit")

        role = input("Select role (1-3): ").strip()

        if role == '1':
            password = input("Enter Teacher Password: ")
            if password == "admin123":
                teacher_menu()
            else:
                print("❌ Incorrect password. Access denied.")
        elif role == '2':
            student_menu()
        elif role == '3':
            print("👋 Thank you for using the system. Goodbye!")
            break
        else:
            print("❌ Invalid selection. Please try again.")

if __name__ == "__main__":
    main()
