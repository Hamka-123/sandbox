import multiprocessing

def main():
    p = multiprocessing.Process(target=lambda x: x + 1, args=(10,))
    p.start()
    p.join()

if __name__ == "__main__":
    main()
