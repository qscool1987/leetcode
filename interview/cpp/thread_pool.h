#ifndef THREAD_POOL_H
#define THREAD_POOL_H

#include <vector>
#include <queue>
#include <memory>
#include <thread>
#include <mutex>
#include <condition_variable>
#include <future>
#include <functional>
#include <stdexcept>

/*
    线程池是个大公司喜欢问的技术点，此处代码是摘录github，并加入了一些注释
    github地址 https://github.com/progschj/ThreadPool
    非常经典，建议深读
*/

class ThreadPool {
public:
    ThreadPool(size_t);
    template<class F, class... Args>
    auto enqueue(F&& f, Args&&... args) 
        -> std::future<typename std::result_of<F(Args...)>::type>;
    ~ThreadPool();
private:
    // need to keep track of threads so we can join them
    std::vector< std::thread > workers; //线程
    // the task queue
    std::queue< std::function<void()> > tasks; //任务队列
    
    // synchronization
    std::mutex queue_mutex;
    std::condition_variable condition;
    bool stop;
};
 
// the constructor just launches some amount of workers
inline ThreadPool::ThreadPool(size_t threads)
    :   stop(false)
{
    for(size_t i = 0;i<threads;++i)
        workers.emplace_back( //加入线程，线程的工作是1.
            [this]
            {
                for(;;) //死循环，不停的从任务队列中取任务 task，执行task()
                {
                    std::function<void()> task;

                    {
                        std::unique_lock<std::mutex> lock(this->queue_mutex); //互斥锁，所有线程互斥访问任务队列，任何时刻只有一个线程访问任务队列
                        this->condition.wait(lock,
                            [this]{ return this->stop || !this->tasks.empty(); }); //条件变量，只有当stop=true 或者任务队列不为空，线程访问任务队列时，任务队列可能为空，为空的时候就让线程等待
                        if(this->stop && this->tasks.empty()) //stop变量用于控制线程池退出
                            return;
                        task = std::move(this->tasks.front());
                        this->tasks.pop();
                    }

                    task();
                }
            }
        );
}

// add new work item to the pool
// 1.任务就是一个函数，或者可调用对象，当然需要支持任意参数和返回类型的任务
// 2.需要将任务包装成无参数形式,加入任务队列，线程获取任务调用 task()就可以，可以通过std::bind将函数和参数进行绑定，再通过
// lambda包装成无参数形式
// 3.线程本质上是和一个函数进行绑定，函数的作用就是不停的从任务队列获取任务，并执行任务
// 当任务队列为空时，线程挂起， 当加入任务时，唤醒线程进行消费
// 由于多个线程访问一个任务队列，所以需要做互斥 mutex
template<class F, class... Args>
auto ThreadPool::enqueue(F&& f, Args&&... args) 
    -> std::future<typename std::result_of<F(Args...)>::type>
{
    using return_type = typename std::result_of<F(Args...)>::type; //F(Args...)的返回类型

    auto task = std::make_shared< std::packaged_task<return_type()> >( 
        //通过lambda和std::packaged_task对 f(args...) 进行包装
            std::bind(std::forward<F>(f), std::forward<Args>(args)...) //包装后的形式为 return_type(), 方便线程获取任务后执行
        );
        //std::packaged_task和get_future
    std::future<return_type> res = task->get_future();
    {
        std::unique_lock<std::mutex> lock(queue_mutex); //往任务队列中加入任务，需要加锁

        // don't allow enqueueing after stopping the pool
        if(stop)
            throw std::runtime_error("enqueue on stopped ThreadPool");

        tasks.emplace([task](){ (*task)(); });
    }
    condition.notify_one();
    return res;
}

// the destructor joins all threads
inline ThreadPool::~ThreadPool()
{
    {
        std::unique_lock<std::mutex> lock(queue_mutex);
        stop = true;
    }
    condition.notify_all();
    for(std::thread &worker: workers)
        worker.join();
}

#endif