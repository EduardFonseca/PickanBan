#create a gui window
import tkinter as tk

if __name__ == '__main__':
    root = tk.Tk()
    root.title('Root Window')

    # Create a frame
    frame = tk.Frame(root, bg='#1a1a1a')
    frame.pack(fill='both', expand=True)

    # Create three buttons within the frame
    button1 = tk.Button(frame, text='Button 1')
    button1.pack(pady=10)

    button2 = tk.Button(frame, text='Button 2')
    button2.pack(pady=10)

    button3 = tk.Button(frame, text='Button 3')
    button3.pack(pady=10)

    root.mainloop()