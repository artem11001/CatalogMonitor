def argv():
    import argparse
    from . import option

    parser = argparse.ArgumentParser(description=f'Example command:\
    --dir=../mysite --dirI="__pycache__ log" --extI=".pyc .log txt"')
    parser.add_argument("--dir", default=option.monitorDir, type=str,
                        help="Catalog monitor")
    parser.add_argument("--diri", default=option.ignortDir, type=str,
                        help="Catalog ignore, optional command")
    parser.add_argument("--exti", default=option.ignoreExt, type=str,
                        help="File ignore, optional command")
    parser.add_argument("--log", default='log', type=str,
                        help="logging directory changes. --log=\
                            /mysdirlog/log.txt or --log=smtp optional command")
    parser.add_argument("--dirBS", default=option.dirBaseShelve, type=str,
                        help="Dir Base shelv")
    args = parser.parse_args()
    monitorDir = args.dir
    dirBaseShelve = args.dirBS
    logging = args.log
    ignortDir = args.diri.split(' ')
    ignoreExt = args.exti.split(' ')
    return {'monitorDir': monitorDir,
            'ignortDir': ignortDir,
            'ignoreExt': ignoreExt,
            'logging': logging,
            'dirBaseShelve': dirBaseShelve}
