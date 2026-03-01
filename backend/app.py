from classes import ResumeRankingSystem, JobDescription
system = ResumeRankingSystem()

while True:
        print("\n===== Transparent Resume Ranking System =====")
        print("1. Insert Job Description")
        print("2. Insert Resumes")
        print("3. Calculate Scores")
        print("4. Show Sorted Results")
        print("5. Reset System")
        print("6. Exit")

        choice = input("Select an option: ")

        if choice == "1":
            if system.job is None:
                system.job = JobDescription()
            
            print("\nPaste the Job Description text below (end with empty line):")
            lines = []
            while True:
                line = input()
                if not line.strip():
                    break
                lines.append(line)
            
            raw_text = " ".join(lines)
            system.job.process_text(raw_text)

        elif choice == "2":
           print("\nEnter path(s) to PDF resume(s), separated by commas:")
           paths = input().split(",")
           paths = [p.strip() for p in paths if p.strip()]
           system.process_resumes(paths)

        elif choice == "3":
            try:
                ranked = system.calculate_scores()
                print("Scoring complete.")
            except Exception as e:
                print(e)

        elif choice == "4":
            system.show_sorted_results()

        elif choice == "5":
            system.reset_system()

        elif choice == "6":
            print("Exiting system.")
            break

        else:
            print("Invalid option. Try again.")

