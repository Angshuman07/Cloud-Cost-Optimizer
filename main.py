import backend
import os

def main_menu():
    while True:
        print("\n" + "="*50)
        print(" 🚀 AI-Powered Cloud Cost Optimizer (Modular Version)")
        print("="*50)
        print("1. 📝 Enter New Project Description")
        print("2. ⚙️  Run Complete Cost Analysis")
        print("3. 📊 View Recommendations")
        print("4. 🚪 Exit")
        
        choice = input("\nEnter choice (1-4): ").strip()
        
        if choice == '1':
            desc = input("\nDescribe your project: ")
            if not desc:
                desc = "We are building a food delivery app for 10,000 users. Budget: 50000 INR. Stack: Node.js, Postgres."
            
            with open("project_description.txt", "w") as f:
                f.write(desc)
            print("✅ Description saved successfully.")
            
        elif choice == '2':
            if not os.path.exists("project_description.txt"):
                print("❌ Please run Option 1 first to create a description.")
                continue
                
            with open("project_description.txt", "r") as f:
                description = f.read()

            profile = backend.generate_profile(description)
            if not profile: continue
            backend.save_json('project_profile.json', profile)

            billing = backend.generate_billing(profile)
            if not billing: continue
            backend.save_json('mock_billing.json', billing)

            report = backend.analyze_costs(profile, billing)
            if not report: continue
            backend.save_json('cost_optimization_report.json', report)
            
            print("\n🎉 Pipeline Completed! Report generated.")

        elif choice == '3':
            report = backend.load_json('cost_optimization_report.json')
            if report:
                print(f"\n📊 Report for: {report.get('project_name')}")
                print(f"💰 Total Cost: ₹{report['analysis']['total_monthly_cost']}")
                print(f"📉 Variance: ₹{report['analysis']['budget_variance']}")
                print("\n💡 Top Recommendations:")
                for rec in report.get('recommendations', [])[:3]:
                    print(f" - {rec['title']} (Save ₹{rec['potential_savings']})")
        
        elif choice == '4':
            print("Goodbye!")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main_menu()