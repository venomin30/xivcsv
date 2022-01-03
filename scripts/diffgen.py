import git
import os
import io
import difflib
import shutil
import sys

repo_root = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..'))
print('repo at \'' + repo_root + '\'')

repo = git.Repo(repo_root)
i_max = len(list(repo.iter_commits('HEAD'))) - 1

with open(os.path.join(repo_root, 'Version.txt'), 'r', encoding='utf-8-sig') as f:
	current_version = f.readline().strip()

print('current version ' + current_version)

for i in range(0, i_max):
	target_head = 'HEAD~' + str(i)
	target_commit = repo.commit(target_head)

	try:
		commit_version_file = target_commit.tree / 'Version.txt'
	except:
		print('Different Version.txt not found')
		quit()

	with io.BytesIO(commit_version_file.data_stream.read()) as f:
		commit_version = f.readline().decode('utf-8-sig').strip()

		if commit_version != current_version:
			break

print('target version ' + commit_version + ' found at ' + target_head)

target_diff = target_commit.diff(None)

diff_root = os.path.join(repo_root, 'diff')
print('writing diff to ' + diff_root)

if (os.path.exists(diff_root)):
	shutil.rmtree(diff_root)

for diff_item in target_diff.iter_change_type('M'):
	if diff_item.b_path[0:4] != 'src/':
		continue

	diff_item_path = diff_item.b_path[4:]
	print(diff_item_path)

	out_path = os.path.join(diff_root, diff_item_path)
	out_dir = os.path.dirname(out_path)
	
	if (not os.path.exists(out_dir)):
		os.makedirs(out_dir)
	
	diff = difflib.ndiff(diff_item.a_blob.data_stream.read().decode('utf-8-sig').splitlines(keepends=True),
			diff_item.b_blob.data_stream.read().decode('utf-8-sig').splitlines(keepends=True))

	with open(out_path, 'w', encoding='utf-8-sig') as f:
		for x in diff:
			if not x.startswith('+ '):
				continue

			out_line = x[2:].strip()

			if (len(out_line) > 0):
				f.write(out_line + '\n')
