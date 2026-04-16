from pathlib import Path


def load_cities(file_path):
    raw_data = Path(file_path).read_bytes()
    text = None

    for encoding in ("utf-8", "utf-16", "cp1252", "latin-1"):
        try:
            text = raw_data.decode(encoding)
            break
        except UnicodeDecodeError:
            continue

    if text is None:
        raise UnicodeDecodeError("decode", b"", 0, 1, "Unable to decode cities file")

    loaded_cities = []
    for line in text.splitlines():
        parts = line.strip().split()
        if len(parts) < 2:
            continue
        try:
            x, y = float(parts[0]), float(parts[1])
            loaded_cities.append((x, y))
        except ValueError:
            # Skip non-numeric lines (e.g., headers/noise) safely.
            continue

    return loaded_cities


cities = load_cities("C:\\Users\\Lenovo\\Desktop\\Sem4\\AI Lab\\Assignment10\\cities (1).txt")

print("total cities:", len(cities))


#distanc efunction function to find squared distance
def distance(c1,c2):
    return(c1[0]-c2[0])**2+(c1[1]-c2[1])**2

def assign_clusters(cities,centers):
    clusters=[[] for _ in centers]
    for city in cities:
        distances=[distance(city,centre) for centre in centers]
        idx=distances.index(min(distances))
        clusters[idx].append(city)
    return clusters


def update_centers(clusters):
    new_centers=[]

    for cluster in clusters:
        if len(cluster)==0:
            new_centers.append((0,0))
            continue
        #here we calculate the mean of x and y coordinates for each cluster to get the new center
        x_mean=sum(city[0] for city in cluster)/len(cluster)
        y_mean=sum(city[1] for city in cluster)/len(cluster)
        new_centers.append((x_mean, y_mean))

    return new_centers


import random

def gradient_descent(cities,k=3,max_iteration=100):
    centers=random.sample(cities,k)

    for _ in range(max_iteration):
        clusters=assign_clusters(cities,centers)
        new_centers=update_centers(clusters)
        if new_centers==centers: #if centers do not change, we have converged
            break

        centers=new_centers

    return centers,clusters


def newton_method(cities,k=3):
    centers=random.sample(cities,k)
    clusters=assign_clusters(cities,centers)
    centers=update_centers(clusters)

    return centers,clusters

def compute_sse(clusters,centers):
    sse=0

    for i,cluster in enumerate(clusters):
        for city in cluster:
            sse+=distance(city,centers[i])

    return sse

# Gradient Descent
centers_gd, clusters_gd = gradient_descent(cities, 3)
sse_gd = compute_sse(clusters_gd, centers_gd)

# Newton Method
centers_nt, clusters_nt = newton_method(cities, 3)
sse_nt = compute_sse(clusters_nt, centers_nt)

print("\n Gradient Descent ")
print("Centers:", centers_gd)
print("SSE:", sse_gd)

print("\n Newton Method ")
print("Centers:", centers_nt)
print("SSE:", sse_nt)

print("\nSimple Comparison")
print("Gradient Descent SSE:", sse_gd)
print("Newton Method SSE:", sse_nt)

if sse_gd < sse_nt:
    diff = ((sse_nt - sse_gd) / sse_nt) * 100 if sse_nt != 0 else 0
    print(f"Gradient Descent is better by {diff:.2f}%")
elif sse_nt < sse_gd:
    diff = ((sse_gd - sse_nt) / sse_gd) * 100 if sse_gd != 0 else 0
    print(f"Newton Method is better by {diff:.2f}%")
else:
    print("Both are equal (same SSE)")
