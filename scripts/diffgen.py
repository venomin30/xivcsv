import git
import os
import io
import shutil
import subprocess
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
		print('Different Version.txt not found in git history')
		quit()

	with io.BytesIO(commit_version_file.data_stream.read()) as f:
		commit_version = f.readline().decode('utf-8-sig').strip()

		if commit_version != current_version:
			break

print('target past version ' + commit_version + ' found at ' + target_head)

print('generating diffs ...', end='\r', flush=True)

try:
	full_diff = subprocess.check_output('git diff ' + target_head + ' --ignore-space-at-eol', stderr=subprocess.STDOUT).decode('utf-8-sig').splitlines()
	full_diff_len_str = str(len(full_diff))
	full_diff_len_str_len = len(full_diff_len_str)
except subprocess.CalledProcessError:
	print('git diff error' + 6 * ' ')
	quit()

diff_root = os.path.join(repo_root, 'diff')
print('writing diffs to ' + diff_root + (3 * ' '))

print('cleaning old diff path ...', end='\r', flush=True)
last_log_len = 26

if (os.path.exists(diff_root)):
	shutil.rmtree(diff_root)
	
current_file = ''

for i, line in enumerate(full_diff):
	line_stripped = line.strip()
	line_len = len(line_stripped)

	if line_len >= 6 and line_stripped[:6] == '+++ b/':
		f.close()
		next_file = line_stripped[6:]

		if not next_file or len(next_file) < 4 or next_file[:4] != 'src/':
			current_file = ''
			continue

		current_file = next_file[4:]
		current_file_output = os.path.join(diff_root, current_file)
		current_out_dir = os.path.dirname(current_file_output)
		if (not os.path.exists(current_out_dir)):
			os.makedirs(current_out_dir)
		
		f = open(current_file_output, 'w', encoding='utf-8-sig')
		continue

	if not current_file or line_len < 2 or line_stripped[0] != '+':
		continue

	f.write(line_stripped[1:] + '\n')

	next_log = 'parsing line ' + str(i).rjust(full_diff_len_str_len) + ' / ' + full_diff_len_str + ' ' + current_file
	next_log_len = len(next_log)
	print(next_log + (' ' * max(0, last_log_len - next_log_len)), end='\r', flush=True)
	last_log_len = next_log_len

print('done' + (' ' * max(0, last_log_len - 4)), flush=True)
