from pipeline.orchestrator import Orchestrator


if __name__ == "__main__":
    orchestrator = Orchestrator()
    metrics = orchestrator.run(
        syscall_tbl="data/kernel_source/arch/riscv/kernel/syscalls/syscall.tbl",
        kconfig="data/kernel_source/.config",
        refined_out_dir="data/syzlang_output/refined",
    )
    print(metrics)
