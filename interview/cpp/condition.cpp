#include <iostream>
#include <vector>
#include <queue>
#include <memory>
#include <thread>
#include <mutex>
#include <condition_variable>
#include "thread_pool.h"

/*
3个线程，一个线程打印0，一个线程打印基数，一个线程打印偶数，
交替输出: 0 1 2 0 3 4 0 5 6 0
*/
int n = 1;
std::condition_variable _cond;
std::mutex _lock;
int flag = 1;

void print_1() {
    while(n < 100) {
        std::unique_lock<std::mutex> lock(_lock);
        _cond.wait(lock, []() {
            return flag == 1;
        });
        std::cout << n << std::endl;
        ++n;
        flag = (flag + 1) % 3;
        _cond.notify_all();
    }
}

void print_2() {
    while(n < 100) {
        std::unique_lock<std::mutex> lock(_lock);
        _cond.wait(lock, []() {
            return flag == 0;
        });
        std::cout << n << std::endl;
        ++n;
        flag = (flag + 1) % 3;
        _cond.notify_all();
    }
}

void print_0() {
    while(n < 100) {
        std::unique_lock<std::mutex> lock(_lock);
        _cond.wait(lock, []() {
            return flag == 2;
        });
        std::cout << 0 << std::endl;
        flag = (flag + 1) % 3;
        _cond.notify_all();
    }
}

template<class F, class... Args>
void task(F&& f, Args&& ...args) {
    auto _task = std::bind(std::forward<F>(f), std::forward<Args>(args)...);
    std::cout << _task() << std::endl;
}

int add(int a, int b) {
    return a + b;
}

int main() {
    task(add, 3 ,5);
    return 0;
}