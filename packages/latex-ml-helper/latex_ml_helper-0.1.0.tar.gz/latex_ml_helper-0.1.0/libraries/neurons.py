def Imports():
    text = """
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import torch
import torch.nn as nn
import torch.optim as optim

from sklearn.metrics import rand_score
from sklearn.cluster import KMeans
from sklearn.mixture import GaussianMixture
from sklearn import datasets
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split
"""
    return text

# Neural network
def data_load():
    text = """
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 42)
X_train.shape

X_train = torch.tensor(X_train, dtype=torch.float)
X_test = torch.tensor(X_test, dtype=torch.float)
y_train = torch.tensor(y_train, dtype=torch.long)
y_test = torch.tensor(y_test, dtype=torch.long)
"""
    return text

def network_and_training():
    text = """
class Classifier(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super().__init__()

        self.linear1 = nn.Linear(input_size, hidden_size)
        self.linear2 = nn.Linear(hidden_size, output_size)
        self.tanh = nn.Tanh()
        self.softmax = nn.Softmax(dim=1)
        
    def forward(self, X):
        out = self.linear1(X)
        out = self.tanh(out)
        out = self.linear2(out)

        return out
    
NUM_EPOCHS = 1000
LR = 1e-3

model = Classifier(4, 10, 3)

loss_fn = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=LR)

model.train()
for epoch in range(1, NUM_EPOCHS + 1):
    y_pred = model(X_train)
    loss = loss_fn(y_pred, y_train)
    
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    if epoch % 100 == 0:
        print(f'Epoch {epoch} avg. loss: {loss.item()}')

model.eval()
y_pred = model(X_test).argmax(dim=1)
print(f'accuraccy: {accuracy_score(y_test, y_pred)}')
print(f'matrica zabune:\n{confusion_matrix(y_test, y_pred)}')
"""
    return text


def loading_batches():
    text = """
from torch.utils.data import Dataset, DataLoader

class ConnectFourDataset(Dataset):
    def __init__(self, fname):
        df = pd.read_csv(fname)
        self.X = torch.tensor(df.drop('class', axis=1).values, dtype=torch.float)
        self.y = torch.tensor(df[['class']].values, dtype=torch.long).squeeze(-1)

    def __len__(self):
        return self.X.shape[0]
    
    def __getitem__(self, idx):
        return self.X[idx], self.y[idx]
    
cf_dataset = ConnectFourDataset('./Podaci/connect-four.csv')
lengths = [int(0.8 * len(cf_dataset)),
         int(0.1 * len(cf_dataset)), 
         len(cf_dataset) - int(0.8 * len(cf_dataset)) - int(0.1 * len(cf_dataset))]
train_dataset, dev_dataset, test_dataset = torch.utils.data.dataset.random_split(cf_dataset, lengths=lengths)

batch_size = 128
train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
dev_loader = DataLoader(dev_dataset, batch_size=batch_size, shuffle=False)
test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)
"""
    return text

def training_loop_batches():
    text = """
def train(model, train_loader, dev_loader, num_epochs=50, lr=1e-3, weight_decay=1e-3, device='cpu'):
    model = model.to(device)
    loss_fn = nn.CrossEntropyLoss()
    optimizer = torch.optim.AdamW(model.parameters(), lr, weight_decay=weight_decay)
    best_dev_loss = 1e9
    for epoch in range(1, num_epochs+1):
        model.train() # pripremi model za treniranje... npr. za racunanje gradijenata
        train_epoch_loss = 0
        
        for i, (X_batch, y_batch) in tqdm(enumerate(train_loader)): # iteriramo po loaderu
            X_batch = X_batch.to(device)
            y_batch = y_batch.to(device)
            y_pred = model(X_batch)
            
            loss = loss_fn(y_pred, y_batch)
            
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            train_epoch_loss += loss.item()
            
        model.eval() # ugasi računanje gradijenata
        dev_epoch_loss = 0
        
        for i, (X_batch, y_batch) in tqdm(enumerate(dev_loader)): # iteriramo po loaderu
            X_batch = X_batch.to(device)
            y_batch = y_batch.to(device)
            y_pred = model(X_batch)
            loss = loss_fn(y_pred, y_batch)
            dev_epoch_loss += loss.item()
            
        print(f'Epoha {epoch}')
        print(f'Prosječan gubitak na skupu za treniranje: {train_epoch_loss / len(train_loader)}')
        print(f'Prosječan gubitak na skupu za validaciju: {dev_epoch_loss / len(dev_loader)}')
        
        if dev_epoch_loss < best_dev_loss:
            best_dev_loss = dev_epoch_loss
            print(f'Spremam stanje modela nakon epohe {epoch}')
            torch.save(model.state_dict(), './model.pt')
"""
    return text

# K-means
def k_means():
    text = """
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs

X, y = make_blobs(n_samples=500, n_features=2, centers=3, random_state=3)

kmeans = KMeans(n_clusters=3).fit(X)
print(f'centri:\n{kmeans.cluster_centers_}')
print(f'oznake:\n{kmeans.labels_}')
print(f'inercija: {kmeans.inertia_}')

plt.scatter(X[:, 0], X[:, 1], c=kmeans.labels_)
"""
    return text

def ch_and_rand_score():
    text = """
from sklearn.metrics import calinski_harabasz_score, rand_score
print(f'CH skor:   {calinski_harabasz_score(X, kmeans.labels_)}')
print(f'Rand skor: {rand_score(y, kmeans.labels_)}')
"""
    return text

def moon_maker():
    text = """
from sklearn.datasets import make_moons
X, y = make_moons(n_samples=100, noise=0.05, random_state=123)
plt.scatter(X[:, 0], X[:, 1], c=y)
"""
    return text

def l1_func():
    text = """
def dist(pi, center):
    res = 0

    for i in range(len(pi)):
        for j in range(len(pi[i])):
            first = abs(center[i][0] - pi[i][j][0])
            second = abs(center[i][1] - pi[i][j][1])
            res += first + second

    return res


dist(pi1, center1), dist(pi2, center2)
"""
    return text

# mixed distributions

def density_function():
    text = """
def fx(x, p, mu, sigma, k):
    l = 0
    for j in range(k):
        l += (p[j] / (sigma[j] * np.sqrt(2 * np.pi))) * np.exp(-(x - mu[j])**2 / (2 * sigma[j]**2))
    return l
"""
    return text

def ploting_mixed():
    text = """
xx = np.linspace(min(X), max(X), 2000)
p = np.array([0.3, 0.7])
mu = np.array([20, 40])
sigma = np.array([5, 5])
k = 2

func = lambda x : fx(x, p, mu, sigma, k)
y = func(xx)

plt.plot(xx, y, label='mixture model')
plt.hist(X, bins=20, density=True)
plt.show()
"""
    return text

def shapiro_wilk():
    text = """
import scipy.stats as stats

shap = stats.shapiro(X)
if shap.pvalue < 0.05:
    print('Podaci nisu normalno distribuirani')
else:
    print(f'Ne možemo tvrditi da podaci nisu normalno distribuirani')
"""
    return text

# gaussian mixture
def gaussian_mixture():
    text = """
model = GaussianMixture(n_components=2, tol=0.001, max_iter=100, n_init=1, init_params='kmeans')
model.fit(X.reshape(-1, 1))

print(f'p: {model.weights_.squeeze()}')
print(f'mu: {model.means_.squeeze()}')
print(f'sigma^2: {model.covariances_.squeeze()}')
print(model.converged_)
print(model.n_iter_)
print(model.lower_bound_)
"""
    return text

def streched_blobs():
    text = """
X, y = make_blobs(n_samples=400, centers=4, cluster_std=0.60, random_state=0)
plt.scatter(X[:,0], X[:,1])
plt.show()

rng = np.random.RandomState(13)
X_stretched = np.dot(X, rng.randn(2, 2))
plt.scatter(X_stretched[:,0], X_stretched[:,1])
plt.show()
"""
    return text

def model_to_samples():
    text = """
X_moons_new, y_moons_new = model.sample(400)
plt.scatter(X_moons_new[:, 0], X_moons_new[:, 1])
"""
    return text

# RNN
def rnn_classifier():
    text = """
class ClassifierRNN(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(ClassifierRNN, self).__init__()

        self.hidden_size = hidden_size

        self.i2h = nn.Linear(input_size + hidden_size, hidden_size)
        self.i2o = nn.Linear(input_size + hidden_size, output_size)
        self.softmax = nn.LogSoftmax(dim=1)

    def forward(self, input, hidden):
        combined = torch.cat((input, hidden), 1)
        hidden = self.i2h(combined)
        output = self.i2o(combined)
        output = self.softmax(output)
        return output, hidden

    def init_hidden(self):
        return torch.zeros(1, self.hidden_size)

n_hidden = 10
rnn_model = ClassifierRNN(n_letters, n_hidden, 4)


output, next_hidden = rnn_model(letter_to_tensor('A'), rnn_model.init_hidden())
print(output)
"""
    return text

def lstm_rnn():
    text = """
pad = nn.utils.rnn.pad_sequence(X, padding_value=69)
lstm = nn.LSTM(input_size=3, hidden_size=20, num_layers=1)
output, (hn, cn) = lstm(pad)
hn
"""
    return text

## teorija

# neuronsk mreža
def activations():
    text = r"""
$$
\sigma:\mathbb{R}\rightarrow(0,1), \; \sigma(x) = \frac{1}{1+e^{-x}}. 
$$

2. Tahn

$$
\mathrm{tanh}: \mathbb{R} \to (-1, 1), \; \mathrm{tanh}(x) = \frac{e^{x}-e^{-x}}{e^{x}+e^{-x}}.
$$

3. ReLu

$$
\mathrm{ReLU}: \mathbb{R} \rightarrow [0,\infty), \; \mathrm{ReLU}(x) =  \mathrm{max}\{0,x\} .
$$
"""
    return text

# klasteri
def kvaz():
    text = r"""
- $d_{LS}(x,y) = ||x-y||^2_2$ (least square (LS) kvazimetrička funkcija)
- $d_1(x,y) = |x-y|$ ($\ell_1$ metrička funkcija, Manhattan metrika)
"""
    return text

def k_krit():
    text = r"""
- zadan je skup $X=\{x^{(i)} \in \mathbb{R}^n: i=1,\cdots,m\}$
- $k\geq 1$
- $\mathcal{F} : \mathcal{P}(X,k) \rightarrow \mathbb{R}_+$ (*suma udaljenosti do centra klastera po svim klasterima*)
- $\mathcal{F}(\Pi) = \sum\limits_{j=1}^{k}\sum\limits_{x^{(i)}\in\pi_j}d(c_j,x^{(i)})$
"""
    return text

def optimization():
    text = r"""
- minimizirati po $ \Pi \in \mathcal{P}(X,k)$
- (globalno) optimalna particija je $\Pi ^* \in \arg\min\limits_{\Pi \in \mathcal{P}(X,k) }{\mathcal{F}(\Pi)}$ 
"""
    return text

def k_pseudo():
    text = r"""
1. odaberi početne centre $c_1, \cdots, c_k$  (*assignment step*)
2. po principu minimalnih udaljenosti odredi klastere $\pi_j = \{x^{(i)}: d(c_j, x^{(i)})\leq d(c_s,x^{(i)}), \forall s=1,\cdots,k\}\; , j=1,\cdots,k$ (*update step*)
3. definiramo nove centre  $c_j \in \arg\min \sum\limits_{x^{(i)}\in \pi_j}d(c_j, x^{(i)})$
4. GOTO 2 ako se novi centri razlikuju od prethodnih
5. RETURN $\pi_1, \dots, \pi_k$
"""
    return text

def ch_score():
    text = r"""
CH = \frac{\frac{1}{k-1}\sum_{j=1}^km_j||c_j - c||^2}{\frac{1}{m-k}\sum_{j=1}^k\sum_{a \in \pi_j}||c_j - a||^2}
$

Veća vrijednost CH skora upućuje na međusobno dobro razdvojene klastere koji su "kompaktni".
"""
    return text

# Soft clustering
def soft_krit():
    text = r"""
$
\Phi(c, W) = \sum_{i=1}^m\sum\limits_{j=1}^k w_{ij}d(c_j, x^{(i)}) 
$
"""
    return text

# log max
def log_max():
    text = r"""
Funkcija cilja -> minimiziramo

$\theta \mapsto \prod\limits_{i=1}^n f_x(x_i,\theta)$ i označavat ćemo je s $L(\theta | x)$

$l = \ln L$

$
l(\theta | x) = \ln{\prod\limits_{i=1}^n f_x(x_i,\theta)} = \sum\limits_{i=1}^n \ln{f_x(x_i,\theta)}
$
"""
    return text

def mixed_gauss():
    text = r"""
funkcija gustoće slučajnih varijabli

 $f_x(\theta,x) = \sum\limits_{j=1}^k p_j \frac{1}{\sigma_j \sqrt{2\pi}}\mathrm{exp}{}\left(\frac{-(x-\mu_j)^2}{2\sigma_j^2}\right)$
- gdje je $\sum_j p_j = 1$ i $p_j \geq 0$ za sve $j$

napadnuta ln

- $\sum\limits_{i=1}^n\ln{}\left(\sum\limits_{j=1}^kp_j \frac{1}{\sigma_j \sqrt{2\pi}}\mathrm{exp}\left(\frac{-(x-\mu_j)^2}{2\sigma_j^2}\right)\right) \rightarrow \max\limits_{\mu,\sigma,p}$  uz uvjet $\sum_j p_j = 1$
"""
    return text

def exploading_grad():
    text = r"""
Rješenje problema eksplodirajućih gradijenata je relativno jednostavno, dovoljno je **podrezati gradijent**, odnosno smanjiti mu vrijednosti kako bi imao neku unaprijed zadanu normu:
$$
g \leftarrow \frac{\alpha g}{||g||}
$$

$$
h_t^{dec}, c_t^{dec} = LSTM(y_t, h_{t-1}^{dec}, c_{t-1}^{dec}).
$$

Za računanje pažnje koristimo sva stanja enkodera:
\begin{align}
e_{t,i} & = h_t^{dec}Wh_i^{enc} \in \mathbb{R}, \quad i=1, \dots, T \\
\alpha_t & = \mathrm{softmax}(e_t) \in \mathbb{R}^T
\end{align}
"""
    return text


def help_code():
    text = """
Imports

# Neural network
data_load - ucitavanje podataka jednostavno
network_and_training - jednostavna mreza i treniranje
load_batches - ucitavanje podataka u batcheve
training_loop_batches - treniranje mreze u batchevima

# K_means
k_means - k_means model i metrike
ch_and_rand_score - CH i rand score
moon_maker - moon distribucija
l1_func - l1 funkcija

# Mixed distribution
density_function - funkcija gustoće za mješovitu distribuciju
ploting_mixed - plotanje mješovite distribucije
shapiro_wilk - shapiro wilk test
gaussian_mixture - model mješovite distribucije
streched_blobs - strechani blobovi
model_to_samples - model u podatke

# RNN
rnn_classifier - RNN klasifikator
lstm_rnn - LSTM
"""
    return text

def help_th():
    text = """
# Neural network
activations - aktivacijske funkcije

# K-means
kvaz - kvazimetrike
k_krit - kriterijska funkcija
optimization - optimizacijski problem
k_pseudo - pseoudo alg. k_means
ch_score - CH skor

# Soft clustering
soft_krit - kriterijska funkcija
log_max - maksimizacija log vjerodojatnosti

# Mixed distribution
mixed_gauss - mješovita distribucija

# RNN
exploading_grad - eksplodirajući gradijenti
"""
    return text