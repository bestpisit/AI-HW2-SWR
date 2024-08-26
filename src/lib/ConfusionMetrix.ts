export function ConfusionMatrix(actual: string[], predicted: string[]) {
    const confusionMatrix = new Map();

    for (let i = 0; i < actual.length; i++) {
        if (!confusionMatrix.has(actual[i] + actual[i])) {
            confusionMatrix.set(actual[i] + actual[i], 0);
        }
        if (!confusionMatrix.has(actual[i] + predicted[i])) {
            confusionMatrix.set(actual[i] + predicted[i], 0);
        }
        if (!confusionMatrix.has(predicted[i] + actual[i])) {
            confusionMatrix.set(predicted[i] + actual[i], 0);
        }
        if (!confusionMatrix.has(predicted[i] + predicted[i])) {
            confusionMatrix.set(predicted[i] + predicted[i], 0);
        }
        confusionMatrix.set(actual[i] + predicted[i], confusionMatrix.get(actual[i] + predicted[i]) + 1);
    }
    return confusionMatrix;
}