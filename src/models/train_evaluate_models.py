import argparse
import os
import time
import json
import numpy as np
import pandas as pd
from typing import Tuple, Dict

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, classification_report
    )
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import RandomForestClassifier, HistGradientBoostingClassifier

RANDOM_STATE = 42

def load_data(csv_path: str) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    if 'label' not in df.columns:
        raise ValueError(
            "Coluna 'label' não encontrada. Adicione uma coluna binária: 0=normal, 1=erro."
        )
    return df

def build_preprocessor(df: pd.DataFrame) -> Tuple[ColumnTransformer, pd.Series, pd.DataFrame]:
    y = df['label']
    X = df.drop(columns=['label'])

    # Opcional: descartar campos que não ajudam (ex.: timestamp bruto).
    if 'timestamp' in X.columns:
        X = X.drop(columns=['timestamp'])

    # Detecta tipos
    numeric_features = X.select_dtypes(include=[np.number]).columns.tolist()
    categorical_features = X.select_dtypes(exclude=[np.number]).columns.tolist()

    # Pré-processamento:
    # - Escalonamento para numéricos (beneficia MLP)
    # - One-hot para categóricos (ex.: 'port' se estiver como string)
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numeric_features),
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
        ],
        remainder='drop'
    )
    return preprocessor, y, X

    def get_models() -> Dict[str, object]:
        # 1) Rede Neural (MLP)
        mlp = MLPClassifier(
            hidden_layer_sizes=(128, 64),
            activation='relu',
            solver='adam',
            alpha=1e-4,
            batch_size=64,
            learning_rate_init=1e-3,
            max_iter=200,
            early_stopping=True,
            n_iter_no_change=10,
            random_state=RANDOM_STATE
        )

        # 2) Random Forest
        rf = RandomForestClassifier(
            n_estimators=300,
            max_depth=None,
            n_jobs=-1,
            random_state=RANDOM_STATE
        )

        # 3) HistGradientBoosting (robusto e rápido)
        hgb = HistGradientBoostingClassifier(
            max_depth=None,
            learning_rate=0.1,
            max_iter=300,
            random_state=RANDOM_STATE
        )

        return {
            'NeuralNet_MLP': mlp,
            'RandomForest': rf,
            'HistGradientBoosting': hgb
        }

    def safe_proba(clf, X):
        # Tenta probability/decision_function para calcular ROC-AUC
        if hasattr(clf, "predict_proba"):
            return clf.predict_proba(X)[:, 1]
        if hasattr(clf, "decision_function"):
            dfc = clf.decision_function(X)
            # Normalização min-max para [0,1] (aprox. para AUC)
            dfc = (dfc - dfc.min()) / (dfc.max() - dfc.min() + 1e-9)
            return dfc
        return None

        def eval_metrics(y_true, y_pred, y_score=None) -> dict:
            m = {
            'accuracy': accuracy_score(y_true, y_pred),
            'precision': precision_score(y_true, y_pred, zero_division=0),
            'recall': recall_score(y_true, y_pred, zero_division=0),
            'f1': f1_score(y_true, y_pred, zero_division=0),
            'confusion_matrix': confusion_matrix(y_true, y_pred).tolist()
            }
        if y_score is not None:
            try:
                m['roc_auc'] = roc_auc_score(y_true, y_score)
            except Exception:
                m['roc_auc'] = float('nan')
        else:
            m['roc_auc'] = float('nan')
        return m

    def main():
        parser = argparse.ArgumentParser(
            description="Treina MLP, RandomForest e HistGradientBoosting para detectar erros em tabelas BMv2."
        )
        parser.add_argument("--csv", required=True, help="Caminho para o CSV (com coluna 'label').")
        parser.add_argument("--outdir", default="./outputs", help="Diretório para salvar modelos e relatórios.")
        args = parser.parse_args()

        os.makedirs(args.outdir, exist_ok=True)

        df = load_data(args.csv)
        preprocessor, y, X = build_preprocessor(df)

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.25, stratify=y, random_state=RANDOM_STATE
        )

        models = get_models()
        rows = []

        for name, core_model in models.items():
            pipe = Pipeline(steps=[('pre', preprocessor), ('clf', core_model)])

            # Tempo de treino
            t0 = time.time()
            pipe.fit(X_train, y_train)
            fit_time = time.time() - t0

            # Predição e tempos
            t1 = time.time()
            y_pred = pipe.predict(X_test)
            pred_time = time.time() - t1

            # Escore para AUC
            try:
                y_score = safe_proba(pipe, X_test)
            except Exception:
                y_score = None

            metrics = eval_metrics(y_test, y_pred, y_score)
            metrics['model'] = name
            metrics['fit_time_s'] = fit_time
            # latência por 1000 amostras (aprox.)
            if len(X_test) > 0:
                metrics['predict_time_ms_per_1k'] = (pred_time / len(X_test)) * 1000 * 1000
            else:
                metrics['predict_time_ms_per_1k'] = float('nan')

            # Salva relatório textual
            report_path = os.path.join(args.outdir, f"{name}_report.txt")
            with open(report_path, "w") as f:
                f.write(classification_report(y_test, y_pred, digits=4, zero_division=0))

            # Salva pipeline treinado
            try:
                import joblib
                joblib.dump(pipe, os.path.join(args.outdir, f"{name}.joblib"))
            except Exception:
                pass

            rows.append({k: v for k, v in metrics.items() if k != 'confusion_matrix'})

            # Confusion matrix JSON (se quiser inspecionar)
            with open(os.path.join(args.outdir, f"{name}_confusion_matrix.json"), "w") as f:
                json.dump({'confusion_matrix': metrics['confusion_matrix']}, f, indent=2)

            print(f"[OK] {name}: acc={metrics['accuracy']:.4f} f1={metrics['f1']:.4f} "
                    f"recall={metrics['recall']:.4f} auc={metrics['roc_auc']:.4f if not np.isnan(metrics['roc_auc']) else float('nan')} "
                    f"fit={fit_time:.2f}s")

        # Tabela consolidada
        metrics_df = pd.DataFrame(rows)
        metrics_csv = os.path.join(args.outdir, "model_metrics.csv")
        metrics_df.to_csv(metrics_csv, index=False)

        print("\nResultados consolidados salvos em:", metrics_csv)
        print(metrics_df.sort_values("f1", ascending=False).to_string(index=False))

    if __name__ == "__main__":
        main()


    #rodar python train_evaluate_models.py --csv caminho/para/sua_tabela.csv --outdir ./outputs
