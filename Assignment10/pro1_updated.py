from pathlib import Path
import random

def load_cities(file_path):
    try:
        raw_data = Path(r"C:\Users\Lenovo\Desktop\Sem4\AI Lab\Assignment10\cities (1).txt").read_bytes()
    except FileNotFoundError:
        return []
    
    text = None
    for encoding in ("utf-8", "utf-16", "cp1252", "latin-1"):
        try:
            text = raw_data.decode(encoding)
            break
        except UnicodeDecodeError:
            continue

    if text is None:
        return []

    loaded_cities = []
    for line in text.splitlines():
        parts = line.strip().split()
        if len(parts) < 2:
            continue
        try:
            x, y = float(parts[0]), float(parts[1])
            loaded_cities.append((x, y))
        except ValueError:
            continue

    return loaded_cities


# Distance (squared)
def distance(c1, c2):
    return (c1[0] - c2[0])**2 + (c1[1] - c2[1])**2


# Assign cities to nearest center
def assign_clusters(cities, centers):
    clusters = [[] for _ in centers]
    for city in cities:
        distances = [distance(city, center) for center in centers]
        idx = distances.index(min(distances))
        clusters[idx].append(city)
    return clusters


# Standard K-means update (mean)
def update_centers_standard(clusters, all_cities):
    new_centers = []
    for cluster in clusters:
        if not cluster:
            new_centers.append(random.choice(all_cities))
            continue
        x_mean = sum(c[0] for c in cluster) / len(cluster)
        y_mean = sum(c[1] for c in cluster) / len(cluster)
        new_centers.append((x_mean, y_mean))
    return new_centers


# Newton-based update (using gradient + second derivative)
def update_centers_newton(clusters, all_cities):
    new_centers = []
    for cluster in clusters:
        if not cluster:
            new_centers.append(random.choice(all_cities))
            continue
        
        # Initialize at mean
        mu_x = sum(c[0] for c in cluster) / len(cluster)
        mu_y = sum(c[1] for c in cluster) / len(cluster)
        
        n = len(cluster)

        # Newton iterations (redundant but for demonstration)
        for _ in range(5):
            grad_x = -2 * sum((c[0] - mu_x) for c in cluster)
            grad_y = -2 * sum((c[1] - mu_y) for c in cluster)

            hess = 2 * n

            mu_x = mu_x - (grad_x / hess)
            mu_y = mu_y - (grad_y / hess)
            
        new_centers.append((mu_x, mu_y))

    return new_centers


# General K-means runner
def run_kmeans(cities, initial_centers, method="standard", max_iter=100):
    centers = list(initial_centers)

    for _ in range(max_iter):
        clusters = assign_clusters(cities, centers)

        if method == "standard":
            new_centers = update_centers_standard(clusters, cities)
        else:
            new_centers = update_centers_newton(clusters, cities)

        if new_centers == centers:
            break

        centers = new_centers

    return centers, clusters


# Compute SSE
def compute_sse(clusters, centers):
    sse = 0
    for i, cluster in enumerate(clusters):
        for city in cluster:
            sse += distance(city, centers[i])
    return sse


# ---------------- MAIN ----------------

cities = load_cities("Lab 10/cities.txt")

if not cities:
    print("No data found.")
else:
    k = 3

    # SAME initialization for fair comparison
    initial_centers = random.sample(cities, k)

    # Gradient Descent (standard K-means)
    centers_gd, clusters_gd = run_kmeans(cities, initial_centers, "standard")
    sse_gd = compute_sse(clusters_gd, centers_gd)

    # Newton Method
    centers_nt, clusters_nt = run_kmeans(cities, initial_centers, "newton")
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

    if abs(sse_gd - sse_nt) < 1e-6:
        print("Both are equal (same SSE)")
    elif sse_gd < sse_nt:
        diff = ((sse_nt - sse_gd) / sse_nt) * 100 if sse_nt != 0 else 0
        print(f"Gradient Descent is better by {diff:.2f}%")
    else:
        diff = ((sse_gd - sse_nt) / sse_gd) * 100 if sse_gd != 0 else 0
        print(f"Newton Method is better by {diff:.2f}%")