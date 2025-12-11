import backend
import os

def main_menu():
    while True:
        print("\n" + "="*50)
        print(" AI-Powered Cloud Cost Optimizer ")
        print("="*50)
        print("1. Enter New Project Description")
        print("2. Run Complete Cost Analysis (Pipeline)")
        print("3. View Recommendations")
        print("4. Exit")
        
        choice = input("\nEnter choice (1-4): ").strip()
        
        if choice == '1':
            print("\nEnter project description (Press Enter for default):")
            desc = input("> ")
            if not desc:
                desc = """We are building a food delivery app for 10,000 users per month. 
                Budget: ₹50,000 per month. 
                Tech stack: Node.js backend, PostgreSQL database, object storage for images, monitoring, and basic analytics. 
                Non-functional requirements: scalability, cost efficiency, uptime monitoring."""
            
            with open("project_description.txt", "w", encoding="utf-8") as f:
                f.write(desc)
            print("✅ Saved to project_description.txt")
            
        elif choice == '2':
            if not os.path.exists("project_description.txt"):
                print("Please run Option 1 first to create a description.")
                continue

            print("\nReading project description...")
            with open("project_description.txt", "r", encoding="utf-8") as f:
                description = f.read()
            
            profile = backend.generate_profile(description)
            if not profile: 
                print("Failed to generate profile. Stopping.")
                continue
            backend.save_json('project_profile.json', profile)

            billing = backend.generate_billing(profile)
            if not billing: 
                print("Failed to generate billing. Stopping.")
                continue
            backend.save_json('mock_billing.json', billing)

            report = backend.analyze_costs(profile, billing)
            if not report: 
                print("Failed to generate report. Stopping.")
                continue
            backend.save_json('cost_optimization_report.json', report)
            
            print("\nPipeline Completed Successfully!")

        elif choice == '3':
            report = backend.load_json('cost_optimization_report.json')
            if report:
                print(f"\nREPORT FOR: {report.get('project_name')}")
                print(f"Total Monthly Cost: ₹{report['analysis']['total_monthly_cost']}")
                print(f"Budget Variance:    ₹{report['analysis']['budget_variance']}")
                
                print("\n💡 TOP RECOMMENDATIONS:")
                for rec in report.get('recommendations', [])[:3]:
                    print(f"\n{rec['title']}")
                    print(f"   Potential Savings: ₹{rec['potential_savings']}")
                    print(f"   Type: {rec['recommendation_type']}")
                    print(f"   Providers: {', '.join(rec.get('cloud_providers', []))}")
            else:
                print("No report found. Please run Option 2 first.")
        
        elif choice == '4':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()