
To load map test1, run:

~ python hashi.py < test1.txt



 #test2.txt
    #..1..
    #.....
    #1...1
    #.....
    #1.2.2
    #add a bridge from between 1...1

    # # test for print_map_with_bridges
    # bridges.append(Bridge((2, 1), (2, 3), 1, 'horizontal'))
    # #test for check_cross
    # print(check_cross(Bridge((1, 2), (3, 2), 1, 'vertical'), bridges))

    # # test for check_islands_connected
    # bridges.append(Bridge((1, 2), (3, 2), 1, 'vertical'))
    # bridges.append(Bridge((3, 0), (3, 0), 1, 'vertical'))
    # bridges.append(Bridge((3, 4), (3, 4), 1, 'vertical'))
    # bridges.append(Bridge((4, 1), (4, 1), 1, 'horizontal'))
    # bridges.append(Bridge((4, 3), (4, 3), 1, 'horizontal'))
    # print(bridges)
    # print(check_islands_connected(5, 5, map, bridges))


    # test for 12
    #test3.txt
    # ..3..
    # .....
    # 3.c.3
    # .....
    # ..3..
    # bridges.append(Bridge((1, 2), (1, 2), 3, 'vertical'))
    # bridges.append(Bridge((3, 2), (3, 2), 3, 'vertical'))
    # bridges.append(Bridge((2, 1), (2, 1), 3, 'horizontal'))
    # bridges.append(Bridge((2, 3), (2, 3), 3, 'horizontal'))
    # print(check_islands_connected(5, 5, map, bridges))