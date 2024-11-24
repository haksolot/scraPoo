import scraping
# test = scraping.scrape_album_infos("https://no1factory.x.yupoo.com")
# for i in range(len(test)):
    # print(test[i])
    
# seller_infos = scraping.scrape_seller_infos("https://no1factory.x.yupoo.com")
# scraping.write_seller_infos(seller_infos, ".")

# album_infos = scraping.scrape_album_infos("https://no1factory.x.yupoo.com")
# scraping.write_album_infos(album_infos, "test")

scraping.create_seller_dir("seller_infos.json", ".")