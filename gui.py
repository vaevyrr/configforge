from __future__ import annotations
import json, tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path
from configforge import load_config, differences, get_path

class App(tk.Tk):
    def __init__(self):
        super().__init__(); self.title("ConfigForge"); self.geometry("1050x700"); self.minsize(800,520); self.build()
    def build(self):
        top=ttk.Frame(self,padding=12);top.pack(fill="x")
        ttk.Label(top,text="ConfigForge",font=("Segoe UI",16,"bold")).pack(anchor="w")
        ttk.Label(top,text="Validate JSON/YAML files, inspect required keys, and compare configurations.").pack(anchor="w",pady=(2,8))
        tabs=ttk.Notebook(self);tabs.pack(fill="both",expand=True,padx=12,pady=(0,12))
        check=ttk.Frame(tabs,padding=12);diff=ttk.Frame(tabs,padding=12);tabs.add(check,text="Validate");tabs.add(diff,text="Compare")
        self.check_path=tk.StringVar();r=ttk.Frame(check);r.pack(fill="x");ttk.Entry(r,textvariable=self.check_path).pack(side="left",fill="x",expand=True);ttk.Button(r,text="Choose",command=lambda:self.choose(self.check_path)).pack(side="left",padx=6);ttk.Button(r,text="Validate",command=self.validate).pack(side="left")
        self.require=tk.StringVar();ttk.Label(check,text="Required keys (comma separated, optional)").pack(anchor="w",pady=(12,2));ttk.Entry(check,textvariable=self.require).pack(fill="x")
        self.check_out=tk.Text(check,wrap="none");self.check_out.pack(fill="both",expand=True,pady=(12,0))
        self.left=tk.StringVar();self.right=tk.StringVar()
        for parent,var,label in ((diff,self.left,"Left file"),(diff,self.right,"Right file")):
            ttk.Label(parent,text=label).pack(anchor="w",pady=(0,2));r=ttk.Frame(parent);r.pack(fill="x",pady=(0,8));ttk.Entry(r,textvariable=var).pack(side="left",fill="x",expand=True);ttk.Button(r,text="Choose",command=lambda v=var:self.choose(v)).pack(side="left",padx=6)
        ttk.Button(diff,text="Compare",command=self.compare).pack(anchor="w")
        self.diff_out=tk.Text(diff,wrap="none");self.diff_out.pack(fill="both",expand=True,pady=(12,0))
    def choose(self,var):
        p=filedialog.askopenfilename(filetypes=[("Config","*.json *.yaml *.yml"),("All files","*.*")])
        if p:var.set(p)
    def validate(self):
        try:
            p=Path(self.check_path.get());data=load_config(p);missing=[x.strip() for x in self.require.get().split(",") if x.strip() and not get_path(data,x.strip())[0]]
            self.check_out.delete("1.0","end");self.check_out.insert("end",f"VALID: {p}\n\n")
            self.check_out.insert("end",json.dumps(data,indent=2,default=str))
            if missing:self.check_out.insert("end","\n\nMISSING REQUIRED KEYS:\n"+ "\n".join(missing))
            else:self.check_out.insert("end","\n\nAll required keys are present.")
        except Exception as e:messagebox.showerror("Validation failed",str(e))
    def compare(self):
        try:
            changes=differences(load_config(Path(self.left.get())),load_config(Path(self.right.get())))
            self.diff_out.delete("1.0","end")
            if not changes:self.diff_out.insert("end","No differences.")
            for kind,key,before,after in changes:self.diff_out.insert("end",f"{kind.upper():7} {key}: {before!r} -> {after!r}\n")
        except Exception as e:messagebox.showerror("Compare failed",str(e))

if __name__=="__main__":App().mainloop()
