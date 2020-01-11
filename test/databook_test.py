"""

Title : databook_test.py
Author : Magnus Fyhr
Created : 1/9/2020

Purpose : To verify the functionality and consistency of the population class.

Development :
    - test_databook         : DONE
    - test_init             : DONE
    - test_step             : DONE
    - test_close            : DONE
    - test_get_databook     : DONE

Testing :
    - test_databook         : DONE
    - test_init             : DONE
    - test_step             : DONE
    - test_close            : DONE
    - test_get_databook     :

"""

import data.driver.databook as db
import data.driver.helper.purifier as puri
import time


def test_databook():

    test_difficulty = 10000

    print()
    print("< TEST > : Testing DataBook : Difficulty = {}.".format(test_difficulty))
    print()

    get_databook_test = test_get_databook(int(test_difficulty/1000))

    init_test = test_init(int(test_difficulty/100))

    step_test = test_step(test_difficulty)

    close_test = test_close(int(test_difficulty/100))

    print()
    print("< TEST > : Done.")
    print()

    # Return Boolean Test Result
    test_result = init_test and step_test and close_test and get_databook_test
    return test_result


def test_init(difficulty):
    sum_time = 0

    # Test Initialization
    init_test = True
    for i in range(difficulty):
        # Execute Initialization, Log Runtime
        start_t = time.time_ns()

        databook = db.DataBook("MSFT")

        end_t = time.time_ns()
        elapsed = end_t - start_t
        sum_time += elapsed

        # Verify Initialization
        if not databook.live:
            init_test = False
            break

    # Calculate Average Runtime
    sum_time /= pow(10, 6)
    per = sum_time / difficulty

    # Print Test Result
    if init_test:
        print("< PASS > : DataBook Initialization : Average {} ms per __init__().".format(per))
    else:
        print("< FAIL > : DataBook Initialization.")

    # Return Boolean Test Result
    return init_test


def test_step(difficulty):
    sum_time = 0

    # Initialize databook for testing
    databook = db.DataBook("MSFT")

    # Test Step
    step_test = True
    fail_data = None
    for i in range(difficulty):
        #if i % 1000 == 0:
        #    databook = db.DataBook("MSFT")

        # Execute Step, Log Runtime
        start_t = time.time_ns()

        data = databook.step()

        end_t = time.time_ns()
        elapsed = end_t - start_t
        sum_time += elapsed

        # Verify Data From Step
        for column_data in puri.pure_columns:
            if data is not None:
                if data is "EOF":
                    databook = db.DataBook("MSFT")
                    break
                elif data[column_data] is None:
                    step_test = False
                    fail_data = data
                    break
            else:
                step_test = False
                fail_data = data
                break

    # Calculate Average Runtime
    per = sum_time / difficulty

    # Print Test Result
    if step_test:
        print("< PASS > : DataBook Step : Average {} ns per step().".format(per))
    else:
        print("< FAIL > : DataBook Step.")
        print("<      > : {}".format(fail_data))

    # Return Boolean Test Result
    return step_test


def test_close(difficulty):
    sum_time = 0

    # Test Close
    close_test = True
    for i in range(difficulty):
        databook = db.DataBook("MSFT")

        # Execute Close, Log Runtime
        start_t = time.time_ns()

        databook.close()

        end_t = time.time_ns()
        elapsed = end_t - start_t
        sum_time += elapsed

        # Verify Initialization
        if databook.live or databook.book is not None:
            close_test = False
            break

    # Calculate Average Runtime
    per = sum_time / difficulty

    # Print Test Result
    if close_test:
        print("< PASS > : DataBook Close : Average {} ns per close().".format(per))
    else:
        print("< FAIL > : DataBook Close.")

    # Return Boolean Test Result
    return close_test


def test_get_databook(difficulty):
    sum_time = 0

    # Test Getting A DataBook
    get_databook_test = True
    for i in range(difficulty):

        # Execute Close, Log Runtime
        start_t = time.time_ns()

        databook = db.get_databook("MSFT")

        end_t = time.time_ns()
        elapsed = end_t - start_t
        sum_time += elapsed

        if not db.verify_databook(databook):
            get_databook_test = False
            break

    # Calculate Average Runtime
    per = sum_time / difficulty

    # Print Test Result
    if get_databook_test:
        print("< PASS > : DataBook Get Data : Average {} ns per close().".format(per))
    else:
        print("< FAIL > : DataBook Get Data.")

    return get_databook_test


