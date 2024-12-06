class DumpBase(object):

    def dump(self, indent_level=0, prefix=""):
        sp = "  " * indent_level + prefix
        for k, value in self.__dict__.items():
            if isinstance(value, DumpBase):
                print(f"{sp}{k}:")
                value.dump(indent_level + 1)
                continue

            if isinstance(value, list) and all([isinstance(a, DumpBase) for a in value]):
                print(f"{sp}{k}:")
                for index, sub_value in enumerate(value):
                    prefix = "- " if index == 0 else "  "
                    sub_value.dump(indent_level + 1, prefix=prefix)
                continue

            print(f"{sp}{k:<22}: {value}")
