
from __future__ import annotations

import math
import random
import statistics as stats
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def simular_uma_replicacao(n: int, lam: float, mu: float, T: float, rng: random.Random):
    """
    Implementação do algoritmo dos slides do Problema 2.

    Retorna:
        x  = número de clientes atendidos
        y  = número de clientes que foram embora sem entrar na fila
        r  = comprimento da fila no instante final
        w  = proporção de clientes que foram embora
        tm = tempo máximo de permanência entre os clientes atendidos
    """
    Tc = 0.0
    gtdisp = [0.0] * n
    ctcheg: list[float] = []

    k = 0
    x = 0
    y = 0
    r = 0
    w = 0.0
    tm = 0.0

    while True:
        z = rng.expovariate(lam)
        if Tc + z > T:
            return x, y, r, w, tm

        Tc += z
        k += 1
        ctcheg.append(Tc)

        while True:
            j = min(range(n), key=lambda idx: gtdisp[idx])
            if not (gtdisp[j] <= Tc and x < k):
                break

            x += 1
            chegada = ctcheg[x - 1]
            a = rng.expovariate(mu)
            gtdisp[j] = max(gtdisp[j], chegada) + a
            tm = max(tm, gtdisp[j] - chegada)

        r = max(0, (k - 1) - x)
        pr = r / (r + n) if r > 0 else 0.0

        if rng.random() < pr:
            k -= 1
            ctcheg.pop()
            y += 1

        r = k - x
        denom = x + y + r
        w = y / denom if denom > 0 else 0.0


def amplitude_ic95(valores) -> float:
    n = len(valores)
    if n <= 1:
        return float("inf")
    return 2 * 1.96 * stats.stdev(valores) / math.sqrt(n)


def estatisticas_basicas(valores):
    arr = np.asarray(valores, dtype=float)
    media = float(np.mean(arr))
    mediana = float(np.median(arr))
    q05 = float(np.quantile(arr, 0.05))
    q25 = float(np.quantile(arr, 0.25))
    q75 = float(np.quantile(arr, 0.75))
    q95 = float(np.quantile(arr, 0.95))
    desvio = float(np.std(arr, ddof=1)) if len(arr) > 1 else 0.0
    return {
        "media": media,
        "mediana": mediana,
        "q05": q05,
        "q25": q25,
        "q75": q75,
        "q95": q95,
        "desvio": desvio,
    }


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


def ecdf(valores):
    arr = np.sort(np.asarray(valores, dtype=float))
    y = np.arange(1, len(arr) + 1) / len(arr)
    return arr, y


def rodar_ate_precisao(
    n, lam, mu, T,
    NB=500,
    alvo_amplitude=0.002,
    seed=20260422,
    max_blocos=2000,
):
    rng = random.Random(seed)

    X, Y, R, W, TM = [], [], [], [], []

    for _ in range(max_blocos):
        for _ in range(NB):
            x, y, r, w, tm = simular_uma_replicacao(n=n, lam=lam, mu=mu, T=T, rng=rng)
            X.append(x)
            Y.append(y)
            R.append(r)
            W.append(w)
            TM.append(tm)

        if amplitude_ic95(W) < alvo_amplitude:
            break
    else:
        raise RuntimeError("Critério de parada não atingido dentro do limite de blocos.")

    return {
        "X": np.array(X, dtype=float),
        "Y": np.array(Y, dtype=float),
        "R": np.array(R, dtype=float),
        "W": np.array(W, dtype=float),
        "TM": np.array(TM, dtype=float),
    }


def grafico_convergencia(ks, medias, li, ls, y_label, titulo, caminho, linha_referencia=None):
    plt.figure(figsize=(11, 6.5))
    plt.plot(ks, medias, label="Média parcial")
    plt.plot(ks, li, linestyle="--", label="LI 95%")
    plt.plot(ks, ls, linestyle="--", label="LS 95%")
    plt.fill_between(ks, li, ls, alpha=0.2)
    if linha_referencia is not None:
        plt.axhline(linha_referencia, linestyle=":", label=f"média final = {linha_referencia:.6f}")
    plt.xlabel("Número de replicações")
    plt.ylabel(y_label)
    plt.title(titulo)
    plt.legend()
    plt.tight_layout()
    plt.savefig(caminho, dpi=180)
    plt.close()


def grafico_histograma(valores, titulo, xlabel, caminho):
    s = estatisticas_basicas(valores)
    plt.figure(figsize=(11, 6.5))
    plt.hist(valores, bins="auto", density=False)
    plt.axvline(s["media"], linestyle="-", label=f"média = {s['media']:.6f}")
    plt.axvline(s["mediana"], linestyle="--", label=f"mediana = {s['mediana']:.6f}")
    plt.axvline(s["q95"], linestyle=":", label=f"quantil 0.95 = {s['q95']:.6f}")
    plt.xlabel(xlabel)
    plt.ylabel("Frequência")
    plt.title(titulo)
    plt.legend()
    plt.tight_layout()
    plt.savefig(caminho, dpi=180)
    plt.close()


def grafico_ecdf(valores, titulo, xlabel, caminho, x_ref=None, y_ref=None):
    x, y = ecdf(valores)
    plt.figure(figsize=(11, 6.5))
    plt.step(x, y, where="post", label="ECDF")
    if x_ref is not None:
        plt.axvline(x_ref, linestyle="--", label=f"referência x = {x_ref:.6f}")
    if y_ref is not None:
        plt.axhline(y_ref, linestyle=":", label=f"referência y = {y_ref:.6f}")
    plt.xlabel(xlabel)
    plt.ylabel("Probabilidade acumulada")
    plt.title(titulo)
    plt.legend()
    plt.tight_layout()
    plt.savefig(caminho, dpi=180)
    plt.close()


def grafico_linha(x, y, titulo, xlabel, ylabel, caminho, hline=None, vline=None):
    plt.figure(figsize=(11, 6.5))
    plt.plot(x, y, marker="o")
    if hline is not None:
        plt.axhline(hline, linestyle="--", label=f"referência = {hline:.6f}")
    if vline is not None:
        plt.axvline(vline, linestyle=":", label=f"n escolhido = {vline}")
    if hline is not None or vline is not None:
        plt.legend()
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(titulo)
    plt.tight_layout()
    plt.savefig(caminho, dpi=180)
    plt.close()


def salvar_texto(caminho: Path, linhas: list[str]):
    caminho.write_text("\n".join(linhas), encoding="utf-8")


def resolver_subproblema_1(output_dir: str | Path, seed=20260422):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    res = rodar_ate_precisao(n=5, lam=3, mu=0.5, T=50, NB=500, alvo_amplitude=0.002, seed=seed)
    X, Y, R, W, TM = res["X"], res["Y"], res["R"], res["W"], res["TM"]

    ks_w, medias_w, li_w, ls_w = medias_parciais_e_ic(W.tolist(), 500)
    ks_tm, medias_tm, li_tm, ls_tm = medias_parciais_e_ic(TM.tolist(), 500)

    grafico_convergencia(
        ks_w, medias_w, li_w, ls_w,
        y_label="W̄_k",
        titulo="Convergência de W_k com intervalo de confiança de 95%",
        caminho=output_dir / "subproblema1_convergencia_W_detalhado.png",
        linha_referencia=float(np.mean(W)),
    )
    grafico_convergencia(
        ks_tm, medias_tm, li_tm, ls_tm,
        y_label="TM̄_k",
        titulo="Convergência de TM_k com intervalo de confiança de 95%",
        caminho=output_dir / "subproblema1_convergencia_TM_detalhado.png",
        linha_referencia=float(np.mean(TM)),
    )

    grafico_histograma(
        W,
        titulo="Histograma detalhado de W",
        xlabel="W",
        caminho=output_dir / "subproblema1_histograma_W_detalhado.png",
    )
    grafico_histograma(
        TM,
        titulo="Histograma detalhado de TM",
        xlabel="TM",
        caminho=output_dir / "subproblema1_histograma_TM_detalhado.png",
    )

    grafico_ecdf(
        W,
        titulo="Função de distribuição empírica acumulada de W",
        xlabel="W",
        caminho=output_dir / "subproblema1_ecdf_W.png",
        x_ref=float(np.quantile(W, 0.95)),
        y_ref=0.95,
    )
    grafico_ecdf(
        TM,
        titulo="Função de distribuição empírica acumulada de TM",
        xlabel="TM",
        caminho=output_dir / "subproblema1_ecdf_TM.png",
        x_ref=13.0,
        y_ref=float(np.mean(TM <= 13.0)),
    )

    resumo = {
        "N_final": int(len(W)),
        "X_barra": float(np.mean(X)),
        "Y_barra": float(np.mean(Y)),
        "R_barra": float(np.mean(R)),
        "W_barra": float(np.mean(W)),
        "TM_barra": float(np.mean(TM)),
        "Pr_d_tm_maior_13": float(np.mean(TM > 13)),
        "ws_quant_0_95_de_w": float(np.quantile(W, 0.95)),
        "amplitude_final_ic95_W": float(amplitude_ic95(W.tolist())),
    }

    w_stats = estatisticas_basicas(W)
    tm_stats = estatisticas_basicas(TM)

    linhas = [
        "SUBPROBLEMA 1",
        f"N final = {resumo['N_final']}",
        f"X̄ = {resumo['X_barra']:.6f}",
        f"Ȳ = {resumo['Y_barra']:.6f}",
        f"R̄ = {resumo['R_barra']:.6f}",
        f"W̄ = {resumo['W_barra']:.6f}",
        f"TM̄ = {resumo['TM_barra']:.6f}",
        f"Pr_d(tm > 13) = {resumo['Pr_d_tm_maior_13']:.6f}",
        f"w_s (quantil 0.95 de w) = {resumo['ws_quant_0_95_de_w']:.6f}",
        f"Amplitude final do IC95% de W = {resumo['amplitude_final_ic95_W']:.6f}",
        "",
        "Resumo adicional de W:",
        f"  mediana = {w_stats['mediana']:.6f}",
        f"  q05 = {w_stats['q05']:.6f}",
        f"  q25 = {w_stats['q25']:.6f}",
        f"  q75 = {w_stats['q75']:.6f}",
        f"  q95 = {w_stats['q95']:.6f}",
        "",
        "Resumo adicional de TM:",
        f"  mediana = {tm_stats['mediana']:.6f}",
        f"  q05 = {tm_stats['q05']:.6f}",
        f"  q25 = {tm_stats['q25']:.6f}",
        f"  q75 = {tm_stats['q75']:.6f}",
        f"  q95 = {tm_stats['q95']:.6f}",
    ]
    salvar_texto(output_dir / "subproblema1_resumo_detalhado.txt", linhas)

    return resumo


def resolver_subproblema_2(output_dir: str | Path, seed_base=20260422, n_max=20):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    linhas = []
    menor_n = None

    for n in range(1, n_max + 1):
        res = rodar_ate_precisao(
            n=n, lam=4, mu=0.5, T=60, NB=500, alvo_amplitude=0.002, seed=seed_base + n
        )
        W = res["W"]

        linha = {
            "n": n,
            "N_final": int(len(W)),
            "W_barra": float(np.mean(W)),
            "Pr_W_menor_igual_0_20": float(np.mean(W <= 0.20)),
            "quantil_0_95_de_W": float(np.quantile(W, 0.95)),
        }
        linhas.append(linha)

        if menor_n is None and linha["Pr_W_menor_igual_0_20"] >= 0.95:
            menor_n = n
            break

    ns = [linha["n"] for linha in linhas]
    medias_W = [linha["W_barra"] for linha in linhas]
    probs = [linha["Pr_W_menor_igual_0_20"] for linha in linhas]
    q95s = [linha["quantil_0_95_de_W"] for linha in linhas]

    grafico_linha(
        ns, medias_W,
        titulo="Média de W por número de guichês",
        xlabel="n",
        ylabel="W̄",
        caminho=output_dir / "subproblema2_media_W_por_n.png",
        hline=0.20,
        vline=menor_n,
    )
    grafico_linha(
        ns, probs,
        titulo="Probabilidade empírica Pr(W ≤ 0.20) por número de guichês",
        xlabel="n",
        ylabel="Pr(W ≤ 0.20)",
        caminho=output_dir / "subproblema2_probabilidade_por_n.png",
        hline=0.95,
        vline=menor_n,
    )
    grafico_linha(
        ns, q95s,
        titulo="Quantil 0.95 de W por número de guichês",
        xlabel="n",
        ylabel="q0.95(W)",
        caminho=output_dir / "subproblema2_quantil95_W_por_n.png",
        hline=0.20,
        vline=menor_n,
    )

    texto = ["SUBPROBLEMA 2", "n,N_final,W_barra,Pr(W<=0.20),quantil_0.95(W)"]
    for linha in linhas:
        texto.append(
            f"{linha['n']},{linha['N_final']},{linha['W_barra']:.6f},"
            f"{linha['Pr_W_menor_igual_0_20']:.6f},{linha['quantil_0_95_de_W']:.6f}"
        )
    if menor_n is None:
        texto.append("Nenhum n em [1,n_max] satisfez Pr(W<=0.20) >= 0.95.")
    else:
        texto.append(f"Menor n que satisfaz Pr(W<=0.20) >= 0.95: {menor_n}")

    salvar_texto(output_dir / "subproblema2_resumo_detalhado.txt", texto)
    return linhas, menor_n


if __name__ == "__main__":
    base = Path("ep1_outputs_revisado")
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
