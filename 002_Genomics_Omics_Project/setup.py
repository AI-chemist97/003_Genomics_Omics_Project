import subprocess
import sys

def install_packages():
    packages = [
        "pandas",
        "numpy",
        "scikit-learn",
        "matplotlib",
        "seaborn",
        "rdkit"
    ]

    for package in packages:
        try:
            print(f"Installing {package}...")

            subprocess.check_call([sys.executable, "-m","pip","install",package])
            print("Succesfully installed {package}.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to install {package}. Error: {e}")
            print("Please try to install it manually using 'pip install {package}'.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    print("Starting environment setup for 'Genomics Omics Project'.")
    install_packages()
    print("Environment setup completed. You are ready for the next step!")