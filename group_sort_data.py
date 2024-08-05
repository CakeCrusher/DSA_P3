import json
import time
import logging
from typing import List, Callable, Dict, Any
from collections import defaultdict

# logging setup
# the logs provide clear documentatuin of every step in the process
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def load_data(file_path: str) -> List[Dict[str, Any]]:
    with open(file_path, "r") as file:
        data = json.load(file)
    return data


def save_data(data: List[Dict[str, Any]], file_path: str):
    with open(file_path, "w") as file:
        json.dump(data, file, indent=2)


def group_by_date(data: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    logger.info("Grouping data by date")
    grouped_data = defaultdict(list)
    for item in data:
        date_key = f"{item['Date']['Year']}-{item['Date']['Month']:02d}"
        grouped_data[date_key].append(item)
    logger.info(f"Grouped data into {len(grouped_data)} unique month-year combination.")
    return dict(grouped_data)


def bubble_sort(arr: List[Any], key_func: Callable[[Any], Any]) -> List[Any]:
    logger.info(f"Starting bubble sort on {len(arr)} items")
    n = len(arr)
    for i in range(n):
        # logging every 1000 iterations
        if i % 1000 == 0:
            logger.info(f"bubble sort progress: {i}/{n} iterations")
        for j in range(0, n - i - 1):
            if key_func(arr[j]) < key_func(arr[j + 1]):
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    logger.info("Bubble Sort completed")
    return arr


def merge_sort(arr: List[Any], key_func: Callable[[Any], Any]) -> List[Any]:
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    # logging every split
    logger.info(f"merge Sort: Splitting array of size {len(arr)}")
    left = merge_sort(arr[:mid], key_func)
    right = merge_sort(arr[mid:], key_func)

    result = merge(left, right, key_func)
    logger.info(f"Merge Sort: Merged array of size {len(result)}")
    return result


def merge(
    left: List[Any], right: List[Any], key_func: Callable[[Any], Any]
) -> List[Any]:
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if key_func(left[i]) >= key_func(right[j]):
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result


def sort_data(
    data: List[Dict[str, Any]], sort_func: Callable, key_func: Callable[[Any], Any]
) -> List[Dict[str, Any]]:
    logger.info(f"Sorting data using {sort_func.__name__}")
    return sort_func(data, key_func)


def sort_months(
    data: Dict[str, List[Dict[str, Any]]], sort_func: Callable
) -> List[Dict[str, List[Dict[str, Any]]]]:
    logger.info(f"Sorting months using {sort_func.__name__}")
    sorted_months = sort_func(
        list(data.items()),
        key_func=lambda x: (int(x[0].split('-')[0]), int(x[0].split('-')[1]))
    )
    return [{"date": date, "data": items} for date, items in sorted_months]


def process_data(
    data: List[Dict[str, Any]], sort_func: Callable
) -> Dict[str, Any]:
    logger.info(f"Processing data using {sort_func.__name__}")
    start_time = time.time()
    # grouping
    grouped_data = group_by_date(data)
    grouping_time = time.time() - start_time
    logger.info(f"Grouping completed in {grouping_time:.2f} seconds")

    sorted_data = {}
    total_sorting_time = 0
    for date, items in grouped_data.items():
        logger.info(f"Sorting data for {date}")
        start_time = time.time()
        # sort data in a per data
        sorted_items = sort_data(items, sort_func, lambda x: x["Data"]["Cases"])
        sorting_time = time.time() - start_time
        total_sorting_time += sorting_time
        sorted_data[date] = sorted_items
        logger.info(
            f"Sorted {len(items)} items for {date} in {sorting_time:.2f} seconds"
        )

    # Sort months
    start_time = time.time()
    sorted_months = sort_months(sorted_data, sort_func)
    month_sorting_time = time.time() - start_time
    total_sorting_time += month_sorting_time
    logger.info(f"Sorted months in {month_sorting_time:.2f} seconds")

    logger.info(f"Total sorting time: {total_sorting_time:.2f} seconds")
    logger.info(
        f"Total processing time: {grouping_time + total_sorting_time:.2f} seconds"
    )

    return {
        "data": sorted_months,
        "metrics": {
            "grouping_time": grouping_time,
            "sorting_time": total_sorting_time,
            "month_sorting_time": month_sorting_time,
            "total_time": grouping_time + total_sorting_time,
            "memory_usage": {
                "input_size": len(json.dumps(data)),
                "output_size": len(json.dumps(sorted_months)),
                "peak_memory": 0,
            },
        },
    }


def main():
    input_file = "covid.json"
    output_file_bubble = "grouped_sorted_covid_bubble.json"
    output_file_merge = "grouped_sorted_covid_merge.json"

    logger.info("Starting COVID data processing")

    data = load_data(input_file)

    logger.info("Processing data with bubble sort")
    bubble_result = process_data(data, bubble_sort)
    logger.info("Processing data with merge sort")
    merge_result = process_data(data, merge_sort)

    save_data(bubble_result, output_file_bubble)
    save_data(merge_result, output_file_merge)
    logger.info("Bubble sort metrics:")
    for key, value in bubble_result["metrics"].items():
        logger.info(f"  {key}: {value}")
    logger.info("Merge sort metrics:")
    for key, value in merge_result["metrics"].items():
        logger.info(f"  {key}: {value}")
    logger.info("Data processing complete")


if __name__ == "__main__":
    main()