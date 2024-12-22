from func import *
import argparse

parser = argparse.ArgumentParser(description="Download content of a Yupoo album page")

parser.add_argument(
    "--link", type=str,
    required=True,
    help="Link of the Yupoo album"
)

parser.add_argument(
    "--output_dir", type=str,
    required=True,
    help="Output directory path"
)

args = parser.parse_args()

def main():
    
    seller_infos = scrape_seller_infos(args.link)
    write_seller_infos(seller_infos, args.output_dir)
    scrape_pages(args.link, args.output_dir + "/" + sanitize_filename(seller_infos['name']))
    
if __name__ == "__main__":
    main()