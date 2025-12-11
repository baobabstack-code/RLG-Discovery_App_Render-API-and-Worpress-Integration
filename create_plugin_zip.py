import zipfile
import os

def create_zip():
    base_dir = r"c:\Work\Simplify Biz\RLG-Discovery_App_Render-API-and-Worpress-Integration\wordpress-plugin"
    src_dir = os.path.join(base_dir, "rlg-discovery-integration")
    output_filename = os.path.join(base_dir, "..", "rlg-discovery-plugin-GUARANTEED.zip")

    print(f"Zipping from: {src_dir}")
    print(f"Output to: {output_filename}")

    with zipfile.ZipFile(output_filename, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(src_dir):
            for file in files:
                abs_path = os.path.join(root, file)
                # Calculate relative path from the base directory (wordpress-plugin)
                # This ensures the files are inside 'rlg-discovery-integration/' in the zip
                rel_path = os.path.relpath(abs_path, base_dir)
                print(f"Adding: {rel_path}")
                zf.write(abs_path, arcname=rel_path)

    print("Zip created successfully.")

if __name__ == "__main__":
    create_zip()
