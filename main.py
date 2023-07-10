import VirtualMouseModule as VMM
import IOModule as IOM

def __init__():
    IOM.printToConsole("Virtual Mouse Project")

def main():
    virtualMouse = VMM.VirtualMouse()
    # virtualMouse.set(paddingX=50, paddingY=50)
    virtualMouse.start()


if __name__ == "__main__":
    main()

