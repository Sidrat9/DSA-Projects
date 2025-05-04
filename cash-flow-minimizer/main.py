import heapq
import tkinter as tk
from tkinter import messagebox, font

def minimize_cash_flow(transactions):
    from collections import defaultdict

    #step:1 calculate net balances
    net_balance = defaultdict(int)
    for frm, to, amount in transactions:
        net_balance[frm] -= amount
        net_balance[to] += amount

    max_heap = [] # People who are owed money (creditors)
    min_heap = []# People who owe money (debtors)

    #step:2 push into heaps
    for person, balance in net_balance.items():
        if balance > 0:
            heapq.heappush(max_heap, (-balance, person)) #Python's heap only gives you the smallest, we negate the balance
        elif balance < 0:
            heapq.heappush(min_heap, (balance, person)) # regular min heap

    #step:3 greedy matching
    result = []
    while max_heap and min_heap:
        credit = heapq.heappop(max_heap)#(-balance, person)
        debit = heapq.heappop(min_heap)#(balance, person)

        settle_amount = min(-debit[0], -credit[0])
        result.append((debit[1], credit[1], settle_amount))

        new_debit = debit[0] + settle_amount
        new_credit = -credit[0] - settle_amount

        if new_debit < 0:
            #If it's still less than 0, the person hasn't fully paid off their debts yet
            heapq.heappush(min_heap, (new_debit, debit[1]))
        if new_credit > 0:
            #new_credit is how much the creditor is still supposed to receive.
            #If > 0, that person hasn’t received full payment yet
            heapq.heappush(max_heap, (-new_credit, credit[1]))
        #And we keep going till all balances are 0
    return result

# for GUI

def run_gui():
    def process_input():
        raw_input = entry.get("1.0", tk.END).strip()
        try:
            lines = raw_input.split('\n')
            tx = []
            for line in lines:
                parts = line.split()
                tx.append([parts[0], parts[1], int(parts[2])])
            output = minimize_cash_flow(tx)
            output_text.set("\n".join([f"{a} pays {b} → {c}" for a, b, c in output]))
        except Exception as e:
            messagebox.showerror("Error", f"Invalid input format!\n{e}")

    root = tk.Tk()
    root.title("💸 Cash Flow Minimizer")
    root.geometry("600x450")
    root.configure(bg="#f0f4f7")

    default_font = font.nametofont("TkDefaultFont")
    default_font.configure(size=11)

    tk.Label(root, text="Enter Transactions (from to amount):", bg="#f0f4f7", font=("Helvetica", 12, "bold")).pack(pady=(15, 5))

    entry = tk.Text(root, height=8, width=60, font=("Consolas", 11))
    entry.pack(padx=20)

    tk.Button(
        root,
        text="🔍 Minimize Cash Flow",
        command=process_input,
        bg="#4CAF50",
        fg="white",
        font=("Helvetica", 11, "bold"),
        padx=10,
        pady=5
    ).pack(pady=15)

    output_text = tk.StringVar()
    tk.Label(
        root,
        text="Optimized Transactions:",
        bg="#f0f4f7",
        font=("Helvetica", 12, "bold"),
        fg="#333"
    ).pack()

    tk.Label(
        root,
        textvariable=output_text,
        bg="#f0f4f7",
        fg="#1a73e8",
        font=("Courier", 11),
        justify="left"
    ).pack(pady=(5, 20))

    root.mainloop()

run_gui()