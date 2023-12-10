# Databricks notebook source
# MAGIC %md
# MAGIC ## creating mount point to blob storage

# COMMAND ----------

dbutils.fs.unmount("/mnt/brewery_blob")

# COMMAND ----------

storage_account_name = "azuremlmvstudy4574453070"
container_name = "brewery"
storage_account_access_key = "mypdVZk5DeW2MmxtcwcCX3YL03Lp4fRGkDytKMtlG/bbl7BaThXJqetBy86pjhB3t6sfFEGta/TE+AStvPfcaQ=="
mount_point = "/mnt/brewery_blob"

dbutils.fs.mount(
  source = f"wasbs://{container_name}@{storage_account_name}.blob.core.windows.net/",
  mount_point = mount_point,
  extra_configs = {f"fs.azure.account.key.{storage_account_name}.blob.core.windows.net": storage_account_access_key}
)

# Access to bronze layer
bronze_path = f"{mount_point}/bronze"

# Access to silver layer
silver_path = f"{mount_point}/silver"

# access to gold layer
gold_path = f"{mount_point}/gold"