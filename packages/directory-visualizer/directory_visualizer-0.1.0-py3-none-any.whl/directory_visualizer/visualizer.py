import os
import argparse

def generate_markdown(directory, markdown_file, depth=None):

    """
    Traverses the given directory and generates a markdown file listing its structure.
    
    :param directory: Path to the directory to visualize.
    :param markdown_file: The file object to write the generated markdown content.
    :param depth: Maximum depth for traversal. If None, no limit is applied.
    """
    def escape_markdown(name):
        """
        Escapes special markdown characters to prevent them from being interpreted as markdown.
        
        :param name: The directory or file name.
        :return: The escaped name as a string.
        """
        special_chars = ['#', '*', '!', '[', ']', '(', ')', '{', '}', '<', '>', '`']
        for char in special_chars:
            name = name.replace(char, f"\\{char}")
        return name

    def traverse_directory(path, level=1, markdown_file=None):
        """
        Recursively traverses the directory and appends its structure to the markdown file.
        
        :param path: Path of the directory or file.
        :param level: Indentation level for directory nesting.
        :param markdown_file: The file object to write the generated markdown content.
        """
        if depth is not None and level > depth:
            return

        indent = "  " * (level - 1)  # Indentation for directories and files
        if os.path.isdir(path):
            markdown_file.write(f"{indent}- {'#' * min(level, 5)} {escape_markdown(os.path.basename(path))}\n")
            for item in os.listdir(path):
                traverse_directory(os.path.join(path, item), level + 1, markdown_file)
        else:
            markdown_file.write(f"{indent}- {escape_markdown(os.path.basename(path))}\n")

    with open(markdown_file, 'w') as md_file:
        md_file.write(f"# Directory Structure of {directory}\n\n")
        traverse_directory(directory, 1, md_file)


def generate_mermaid(directory, mermaid_file, depth=None):
    """
    Traverses the given directory and generates a Mermaid flowchart for the directory structure.
    
    :param directory: Path to the directory to visualize.
    :param mermaid_file: The file object to write the generated Mermaid content.
    :param depth: Maximum depth for traversal. If None, no limit is applied.
    """
    def escape_mermaid(name):
        """
        Escapes special characters for Mermaid syntax to prevent rendering issues.
        
        :param name: The directory or file name.
        :return: The escaped name as a string.
        """
        special_chars = ['(', ')', '{', '}', '[', ']', '#', '.', ',', ';']
        for char in special_chars:
            name = name.replace(char, f"\\{char}")
        return name
    
    def regenerate_filename(name):
        """
        Regenerates the filename by replacing spaces with underscores and ensuring compatibility
        with Mermaid syntax.

        :param name: The original file name.
        :return: The regenerated file name.
        """
        return name.replace(" ", "_").replace(".", "_").replace("-", "_")
    
    def traverse_directory(path, level=1, mermaid_file=None, parent_dir=None):
        """
        Recursively traverses the directory and appends its structure to the Mermaid file.
        
        :param path: Path of the directory or file.
        :param level: Indentation level for directory nesting.
        :param mermaid_file: The file object to write the generated Mermaid content.
        :param parent_dir: The parent directory node (used for linking).
        """
        if depth is not None and level > depth:
            return

        indent = "  " * level  # Indentation for directories and files
        node_name = escape_mermaid(os.path.basename(path))

        if os.path.isdir(path):
            dir_name = regenerate_filename(node_name)
            if parent_dir:
                mermaid_file.write(f"{indent}{parent_dir} --> {dir_name}[( {node_name} )]\n")
            else:
                mermaid_file.write(f"{indent}{dir_name}[( {node_name} )]\n")
            
            for item in os.listdir(path):
                item_path = os.path.join(path, item)
                traverse_directory(item_path, level + 1, mermaid_file, dir_name)
        else:
            file_name = regenerate_filename(node_name)
            mermaid_file.write(f"{indent}{parent_dir} --> {file_name}[( {node_name} )]\n")

    with open(mermaid_file, 'w') as mermaid:
        mermaid.write("```mermaid\n")
        mermaid.write("graph TD\n")  # Top-down flowchart
        traverse_directory(directory, 1, mermaid)
        mermaid.write("```")


def run_visualizer():
    """
    Entry point for the CLI with additional features.
    """
    parser = argparse.ArgumentParser(description="Directory Visualizer CLI")
    parser.add_argument('-p', '--path', help="Path to the directory you want to visualize", required=True)
    parser.add_argument('-f', '--format', choices=['markdown', 'mermaid'], help="Output format (markdown or mermaid)", default='markdown')
    parser.add_argument('-o', '--output', help="Output file path to save the visualization")
    parser.add_argument('--depth', type=int, help="Limit directory traversal depth (optional)")
    parser.add_argument('--raw-mermaid', action='store_true', help="Save Mermaid diagram as a raw .mmd file")

    args = parser.parse_args()

    # If the output file is not specified, use a default filename
    if not args.output:
        if args.format == 'markdown':
            args.output = "directory_structure.md"
        else:
            # For Mermaid format, decide based on raw-mermaid flag
            if args.raw_mermaid:
                args.output = "directory_structure.mmd"
            else:
                args.output = "directory_structure.md"

    # Validate the directory path
    if not os.path.isdir(args.path):
        print(f"The specified path '{args.path}' is not a valid directory.")
        return

    # Generate the appropriate file format
    if args.format == 'markdown':
        generate_markdown(args.path, args.output, args.depth)
        print(f"Directory structure saved in markdown format to {args.output}")
    else:
        generate_mermaid(args.path, args.output, args.depth)
        if args.raw_mermaid:
            print(f"Directory structure saved as raw Mermaid format to {args.output}")
        else:
            print(f"Directory structure saved in Mermaid format (with Markdown support) to {args.output}")
def main():
    run_visualizer()

if __name__ == "__main__":
    main()