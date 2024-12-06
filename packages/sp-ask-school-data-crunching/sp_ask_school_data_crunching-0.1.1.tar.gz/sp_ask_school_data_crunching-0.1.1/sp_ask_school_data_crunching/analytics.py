


from datetime import datetime, timedelta
import lh3.api

def get_chats_between_dates(start_date: str, end_date: str):
    """
    Get chats between two dates using LibraryH3lp API
    
    Args:
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
    """
    # Initialize client
    client = lh3.api.Client()
    
    # Convert strings to datetime objects
    start_dt = datetime.strptime(start_date, "%Y-%m-%d")
    end_dt = datetime.strptime(end_date, "%Y-%m-%d")
    
    all_chats = []
    current_date = start_dt
    
    while current_date <= end_dt:
        try:
            # Get chats for current day
            daily_chats = client.chats().list_day(
                current_date.year,
                current_date.month,
                current_date.day
            )
            
            if daily_chats:
                all_chats.extend(daily_chats)
                print(f"Fetched {len(daily_chats)} chats for {current_date.date()}")
                
        except Exception as e:
            print(f"Error fetching data for {current_date.date()}: {str(e)}")
            
        # Move to next day
        current_date += timedelta(days=1)
    
    print(f"\nTotal chats fetched: {len(all_chats)}")
    return all_chats

# Example usage
if __name__ == "__main__":
    chats = get_chats_between_dates("2016-11-25", "2024-12-01")
    
    # Example analysis
    ended_chats = [chat for chat in chats if chat['ended']]
    accepted_chats = [chat for chat in chats if chat['accepted']]
    
    print(f"\nAnalysis:")
    print(f"Total chats: {len(chats)}")
    print(f"Ended chats: {len(ended_chats)}")
    print(f"Accepted chats: {len(accepted_chats)}")

    