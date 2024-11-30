import requests
import time
import threading
import argparse

def send_request(url, results):
    """Mengirimkan satu request ke URL dan mencatat waktu respon."""
    try:
        start_time = time.time()
        response = requests.get(url)
        end_time = time.time()

        # Mencatat waktu respons dan status code
        results.append({
            "status_code": response.status_code,
            "response_time": end_time - start_time
        })
    except Exception as e:
        results.append({
            "status_code": None,
            "response_time": None,
            "error": str(e)
        })

def load_test(url, num_requests, num_threads):
    """Melakukan load testing dengan mengirimkan sejumlah request ke URL tertentu."""
    results = []
    threads = []

    print(f"Memulai load test ke {url} dengan {num_requests} permintaan menggunakan {num_threads} thread...\n")

    # Membagi permintaan berdasarkan thread
    requests_per_thread = num_requests // num_threads

    for i in range(num_threads):
        thread = threading.Thread(
            target=lambda: [send_request(url, results) for _ in range(requests_per_thread)]
        )
        threads.append(thread)

    # Memulai semua thread
    for thread in threads:
        thread.start()

    # Menunggu semua thread selesai
    for thread in threads:
        thread.join()

    print("Load testing selesai.\n")
    return results

def analyze_results(results):
    """Menganalisis hasil load testing."""
    response_times = [r["response_time"] for r in results if r["response_time"] is not None]
    success_count = len([r for r in results if r["status_code"] == 200])
    failure_count = len(results) - success_count

    print("Ringkasan Hasil Load Testing:")
    print(f"  Total Permintaan   : {len(results)}")
    print(f"  Berhasil (200 OK)  : {success_count}")
    print(f"  Gagal              : {failure_count}")
    if response_times:
        print(f"  Waktu Respon Rata-rata: {sum(response_times) / len(response_times):.2f} detik")
        print(f"  Waktu Respon Terkecil : {min(response_times):.2f} detik")
        print(f"  Waktu Respon Terbesar : {max(response_times):.2f} detik")
    else:
        print("  Tidak ada data waktu respon yang tersedia.")

# if __name__ == "__main__":
#     # URL target
#     target_url = input("Masukkan URL target (contoh: https://example.com): ")

#     # Jumlah permintaan total dan thread
#     total_requests = int(input("Masukkan jumlah total permintaan: "))
#     total_threads = int(input("Masukkan jumlah thread yang akan digunakan: "))

#     # Melakukan load test
#     results = load_test(target_url, total_requests, total_threads)

#     # Menganalisis hasil
#     analyze_results(results)

import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Load testing script")
    parser.add_argument("url", type=str, help="Target URL for load testing")
    parser.add_argument("total_requests", type=int, help="Total number of requests")
    parser.add_argument("total_threads", type=int, help="Number of threads to use")

    args = parser.parse_args()

    # Melakukan load test
    results = load_test(args.url, args.total_requests, args.total_threads)

    # Menganalisis hasil
    analyze_results(results)
