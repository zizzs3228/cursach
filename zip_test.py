import archive_management
import asyncio

path = "./6281213964523.rar"
test_user = "1234567"
async def main():
    #zip_management.zip_extract(test_user, path)
    await archive_management.archive_extract(test_user, path)



if __name__ == "__main__":
    asyncio.run(main())