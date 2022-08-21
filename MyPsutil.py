import psutil as ps


class MyPsutil:

    @staticmethod
    def show_activate_processess():
        process_set = set()

        for proc in ps.process_iter():
            info = proc.as_dict(attrs=['pid', 'name'])
            process_set.add(info['name'])
        return sorted(process_set)

