
from __future__ import annotations

import math
import random
import statistics as stats
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


# ============================================================
# Simulação de uma realização, exatamente como nos slides
# do Problema 2 ("Sistema de atendimento com clientes impacientes")
# ============================================================

def simular_uma_replicacao(n: int, lam: float, mu: float, T: float, rng: random.Random):
    """
    Retorna (x, y, r, w, tm), conforme os slides:
      x  = número de clientes atendidos
      y  = número de clientes que foram embora sem entrar na fila
      r  = comprimento da fila no instante final
      w  = proporção de clientes que foram embora
      tm = tempo máximo de permanência entre os clientes atendidos
    """

    Tc = 0.0
    gtdisp = [0.0] * n
    ctcheg = []

    k = 0   # clientes que entraram na fila até o momento
    x = 0   # clientes atendidos
    y = 0   # clientes que foram embora
    r = 0
    w = 0.0
    tm = 0.0

    expovariate = rng.expovariate
    randomf = rng.random

    while True:
        z = expovariate(lam)
        if Tc + z > T:
            return x, y, r, w, tm

        Tc += z
        k += 1
        ctcheg.append(Tc)

        # Enquanto algum guichê ficar livre até Tc e ainda houver cliente a processar
        while True:
            minv = gtdisp[0]
            j = 0
            for idx in range(1, n):
                v = gtdisp[idx]
                if v < minv:
                    minv = v
                    j = idx

            if not (minv <= Tc and x < k):
                break

            x += 1
            chegada_cliente = ctcheg[x - 1]
            inicio_atendimento = max(minv, chegada_cliente)
            tempo_servico = expovariate(mu)
            fim = inicio_atendimento + tempo_servico
            gtdisp[j] = fim

            permanencia = fim - chegada_cliente
            if permanencia > tm:
                tm = permanencia

        # comprimento da fila sem considerar o cliente que acabou de chegar
        r = max(0, (k - 1) - x)

        pr = r / (r + n) if r > 0 else 0.0
        if randomf() < pr:
            k -= 1
            ctcheg.pop()
            y += 1

        r = k - x
        denom = x + y + r
        w = y / denom if denom > 0 else 0.0


def amplitude_ic95(valores):
    n = len(valores)
    if n <= 1:
        return float("inf")
    s = stats.stdev(valores)
    return 2 * 1.96 * s / math.sqrt(n)


def medias_parciais_e_ic(valores, bloco):
    ks, medias, li, ls = [], [], [], []
    for k in range(bloco, len(valores) + 1, bloco):
        prefixo = valores[:k]
        media = float(np.mean(prefixo))
        semi = 1.96 * stats.stdev(prefixo) / math.sqrt(k) if k > 1 else 0.0
        ks.append(k)
        medias.append(media)
        li.append(media - semi)
        ls.append(media + semi)
    return ks, medias, li, ls


def rodar_ate_precisao(n, lam, mu, T, NB=500, alvo_amplitude=0.002, seed=20260422):
    rng = random.Random(seed)

    X, Y, R, W, TM = [], [], [], [], []

    while True:
        for _ in range(NB):
            x, y, r, w, tm = simular_uma_replicacao(n=n, lam=lam, mu=mu, T=T, rng=rng)
            X.append(x)
            Y.append(y)
            R.append(r)
            W.append(w)
            TM.append(tm)

        if amplitude_ic95(W) < alvo_amplitude:
            break

    return {
        "X": np.array(X, dtype=float),
        "Y": np.array(Y, dtype=float),
        "R": np.array(R, dtype=float),
        "W": np.array(W, dtype=float),
        "TM": np.array(TM, dtype=float),
    }


def resolver_subproblema_1(output_dir: str | Path, seed=20260422):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    res = rodar_ate_precisao(n=5, lam=3, mu=0.5, T=50, NB=500, alvo_amplitude=0.002, seed=seed)
    X, Y, W, TM = res["X"], res["Y"], res["W"], res["TM"]

    ks_w, medias_w, li_w, ls_w = medias_parciais_e_ic(W.tolist(), 500)
    ks_tm, medias_tm, li_tm, ls_tm = medias_parciais_e_ic(TM.tolist(), 500)

    plt.figure(figsize=(10, 6))
    plt.plot(ks_w, medias_w, label="Média parcial de W")
    plt.plot(ks_w, li_w, linestyle="--", label="LI 95%")
    plt.plot(ks_w, ls_w, linestyle="--", label="LS 95%")
    plt.xlabel("N")
    plt.ylabel("W̄_k")
    plt.title("Convergência de W_k")
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_dir / "subproblema1_convergencia_W.png", dpi=160)
    plt.close()

    plt.figure(figsize=(10, 6))
    plt.plot(ks_tm, medias_tm, label="Média parcial de TM")
    plt.plot(ks_tm, li_tm, linestyle="--", label="LI 95%")
    plt.plot(ks_tm, ls_tm, linestyle="--", label="LS 95%")
    plt.xlabel("N")
    plt.ylabel("TM̄_k")
    plt.title("Convergência de TM_k")
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_dir / "subproblema1_convergencia_TM.png", dpi=160)
    plt.close()

    plt.figure(figsize=(10, 6))
    plt.hist(W, bins=30)
    plt.xlabel("W")
    plt.ylabel("Frequência")
    plt.title("Histograma de W")
    plt.tight_layout()
    plt.savefig(output_dir / "subproblema1_histograma_W.png", dpi=160)
    plt.close()

    plt.figure(figsize=(10, 6))
    plt.hist(TM, bins=30)
    plt.xlabel("TM")
    plt.ylabel("Frequência")
    plt.title("Histograma de TM")
    plt.tight_layout()
    plt.savefig(output_dir / "subproblema1_histograma_TM.png", dpi=160)
    plt.close()

    resumo = {
        "N_final": int(len(W)),
        "X_barra": float(np.mean(X)),
        "Y_barra": float(np.mean(Y)),
        "W_barra": float(np.mean(W)),
        "TM_barra": float(np.mean(TM)),
        "Pr_d_tm_maior_13": float(np.mean(TM > 13)),
        "ws_quant_0_95_de_w": float(np.quantile(W, 0.95)),
        "amplitude_final_ic95_W": float(amplitude_ic95(W.tolist())),
    }

    texto = []
    texto.append("SUBPROBLEMA 1")
    texto.append(f"N final = {resumo['N_final']}")
    texto.append(f"X̄ = {resumo['X_barra']:.6f}")
    texto.append(f"Ȳ = {resumo['Y_barra']:.6f}")
    texto.append(f"W̄ = {resumo['W_barra']:.6f}")
    texto.append(f"TM̄ = {resumo['TM_barra']:.6f}")
    texto.append(f"Pr_d(tm > 13) = {resumo['Pr_d_tm_maior_13']:.6f}")
    texto.append(f"w_s (quantil 0.95 de w) = {resumo['ws_quant_0_95_de_w']:.6f}")
    texto.append(f"Amplitude final do IC95% de W = {resumo['amplitude_final_ic95_W']:.6f}")
    (output_dir / "subproblema1_resumo.txt").write_text("\n".join(texto), encoding="utf-8")

    return resumo


def resolver_subproblema_2(output_dir: str | Path, seed_base=20260422):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    linhas = []
    menor_n = None

    for n in range(1, 21):
        res = rodar_ate_precisao(
            n=n, lam=4, mu=0.5, T=60, NB=500, alvo_amplitude=0.002, seed=seed_base + n
        )
        W = res["W"]
        prob = float(np.mean(W <= 0.20))

        linha = {
            "n": n,
            "N_final": int(len(W)),
            "W_barra": float(np.mean(W)),
            "Pr_W_menor_igual_0_20": prob,
            "quantil_0_95_de_W": float(np.quantile(W, 0.95)),
        }
        linhas.append(linha)

        if menor_n is None and prob >= 0.95:
            menor_n = n
            break

    texto = ["SUBPROBLEMA 2", "n,N_final,W_barra,Pr(W<=0.20),quantil_0.95(W)"]
    for linha in linhas:
        texto.append(
            f"{linha['n']},{linha['N_final']},{linha['W_barra']:.6f},"
            f"{linha['Pr_W_menor_igual_0_20']:.6f},{linha['quantil_0_95_de_W']:.6f}"
        )
    if menor_n is None:
        texto.append("Nenhum n em [1,20] satisfez Pr(W<=0.20) >= 0.95.")
    else:
        texto.append(f"Menor n que satisfaz Pr(W<=0.20) >= 0.95: {menor_n}")

    (output_dir / "subproblema2_resumo.txt").write_text("\n".join(texto), encoding="utf-8")

    return linhas, menor_n


if __name__ == "__main__":
    base = Path("ep1_outputs")
    base.mkdir(exist_ok=True)

    sp1 = resolver_subproblema_1(base / "subproblema1")
    linhas, menor_n = resolver_subproblema_2(base / "subproblema2")

    print("Subproblema 1:")
    for k, v in sp1.items():
        print(f"  {k}: {v}")

    print("\nSubproblema 2:")
    for linha in linhas:
        print(linha)
    print(f"\nMenor n: {menor_n}")
